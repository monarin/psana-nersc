## user_callbacks_pipe
From documentation.pdf page 34, we can supply different callbacks to the start (cb_start), receving event (cb_dld_event), and end (cb_end) phases. Below shows a modified version:
```
#include <stdio.h>
#include <stdlib.h>
#include <scTDC.h>
#include <inttypes.h>
struct sc_DeviceProperties3 sizes;

struct PrivData {
    int cn_measures;
    int cn_tdc_events;
    int cn_dld_events;
    double total_time;
};

/* Include an actual Semaphore implementation, such as in
   * https://github.com/preshing/cpp11-on-multicore/blob/master/common/sema.h
   */
#ifndef __CPP11OM_SEMAPHORE_H__
#define __CPP11OM_SEMAPHORE_H__

#include <atomic>
#include <cassert>
//---------------------------------------------------------
// Semaphore (POSIX, Linux)
//---------------------------------------------------------

#include <semaphore.h>

class Semaphore
{
private:
    sem_t m_sema;

    Semaphore(const Semaphore& other) = delete;
    Semaphore& operator=(const Semaphore& other) = delete;

public:
    Semaphore(int initialCount = 0)
    {
        assert(initialCount >= 0);
        sem_init(&m_sema, 0, initialCount);
    }

    ~Semaphore()
    {
        sem_destroy(&m_sema);
    }

    void wait()
    {
        // http://stackoverflow.com/questions/2013181/gdb-causes-sem-wait-to-fail-with-eintr-error
        int rc;
        do
        {
            rc = sem_wait(&m_sema);
        }
        //while (rc == -1 && errno == EINTR);
        while (rc == -1);
    }

    void signal()
    {
        sem_post(&m_sema);
    }

    void signal(int count)
    {
        while (count-- > 0)
        {
            sem_post(&m_sema);
        }
    }
};
#endif // __CPP11OM_SEMAPHORE_H__

Semaphore sem;

void cb_start(void *p) {
    /* this function gets called every time a measurement starts */
    struct PrivData *priv_data = (struct PrivData *)p; 
    printf("START cn_measures: %d\n", priv_data->cn_measures);
}
void cb_end(void *p) {
    /* this function gets called every time a measurement finishes */
    struct PrivData *priv_data = (struct PrivData *)p; 
    priv_data->cn_measures++;
    printf("END cn_measures: %d\n", priv_data->cn_measures);
    sem.signal();
}
void cb_millis(void *p) {
    /* this function gets called every time a millisecond has ellapsed as
       * tracked by the hardware */
}
void cb_stat(void *p, const struct statistics_t *stat) {
    /* this function gets called every time statistics data is received,
       * usually at the end of every measurement, but before the end-of-measurement
       * callback */
}
void cb_tdc_event
(void *priv,
 const struct sc_TdcEvent *const event_array,
 size_t event_array_len)
{
    struct PrivData *priv_data = (struct PrivData *)priv; 
    priv_data->cn_tdc_events++;
    printf("TDCEVENT: %d\n", priv_data->cn_tdc_events);
    const char *buffer = (const char *) event_array;
    size_t j;
    for (j=0; j<event_array_len; ++j) {
        const struct sc_TdcEvent *obj =
            (const struct sc_TdcEvent *)(buffer + j * sizes.tdc_event_size);
        /* insert code here, that uses the TDC event data.
           * obj->channel, obj->time_data ... contain information about
           * the j-th TDC event provided during this call. */
        int channel = obj->channel;
        uint32_t time_data = obj->time_data;
        printf("event %d --> channel: %d time_data: %" PRIu32 "\n", j, channel, time_data);
    }
}
void cb_dld_event
(void *priv,
const struct sc_DldEvent *const event_array,
size_t event_array_len)
{
    struct PrivData *priv_data = (struct PrivData *)priv; 
    priv_data->cn_dld_events++;
    printf("DLDEVENT: %d\n", priv_data->cn_dld_events);
    const char *buffer = (const char *) event_array;
    size_t j;
    for (j=0; j<event_array_len; ++j) {
        const struct sc_DldEvent *obj =
            (const struct sc_DldEvent *)(buffer + j * sizes.dld_event_size);
        /* insert code here, that uses the DLD event data.
        * obj->dif1, obj->dif2, obj->sum ... contain information about
        * the j-th DLD event provided during this call. */
        unsigned long long start_counter = obj->start_counter;
        unsigned long long time_tag = obj->time_tag; 
        unsigned subdevice = obj->subdevice;
        unsigned channel = obj->channel;
        unsigned long long sum = obj->sum; 
        unsigned short dif1 = obj->dif1;
        unsigned short dif2 = obj->dif2;
        unsigned master_rst_counter = obj->master_rst_counter;
        unsigned short adc = obj->adc;
        unsigned short signal1bit = obj->signal1bit;
        unsigned long _low = time_tag & 0xffffffff;
        unsigned long _high = (time_tag >> 32) & 0xffffffff;
        printf("  j: %d timetag: %llu (%lu.%lu) sum: %llu dif1: %hu dif2: %hu\n", j, time_tag, _high, _low, sum, dif1, dif2);

    }
}

int main()
{
    int dd;
    int ret;
    struct PrivData priv_data = {0, 0, 0, 0.0};
    char *buffer;
    struct sc_pipe_callbacks *cbs;
    struct sc_pipe_callback_params_t params;
    int pd;
    dd = sc_tdc_init_inifile("tdc_gpx3.ini");
    if (dd < 0) {
        char error_description[ERRSTRLEN];
        sc_get_err_msg(dd, error_description);
        printf("error! code: %d, message: %s\n", dd, error_description);
        return dd;
    }
    ret = sc_tdc_get_device_properties(dd, 3, &sizes);
    if (ret < 0) {
        char error_description[ERRSTRLEN];
        sc_get_err_msg(ret, error_description);
        printf("error! code: %d, message: %s\n", ret, error_description);
        return ret;
    }
    buffer = (char*) calloc(1, sizes.user_callback_size);
    cbs = (struct sc_pipe_callbacks *)buffer;
    cbs->priv = &priv_data;
    cbs->start_of_measure = cb_start;
    cbs->end_of_measure = cb_end;
    cbs->millisecond_countup = cb_millis;
    cbs->statistics = cb_stat;
    cbs->tdc_event = cb_tdc_event;
    cbs->dld_event = cb_dld_event;
    params.callbacks = cbs;
    pd = sc_pipe_open2(dd, USER_CALLBACKS, &params);
    if (pd < 0) {
        char error_description[ERRSTRLEN];
        sc_get_err_msg(pd, error_description);
        printf("error! code: %d, message: %s\n", pd, error_description);
        return pd;
    }
    free(buffer);
    ret = sc_tdc_start_measure2(dd, 1000);
    if (ret < 0) {
        char error_description[ERRSTRLEN];
        sc_get_err_msg(ret, error_description);
        printf("error! code: %d, message: %s\n", ret, error_description);
        return dd;
    }
    /* Wait until the semaphore is signalled, which happens in our callback for
       * the end-of-measurement event */
    sem.wait();
    sc_pipe_close2(dd, pd);
    sc_tdc_deinit2(dd);
    return 0;
}

```
To compile the code, source lcls2/setup_env.sh and
```
g++ user_callbacks_pipe.cc -I/opt/kmicro/include -L/opt/kmicro/lib -lscTDC -L$CONDA_PREFIX/lib -ltiff -lsqlite3 -o u    ser_callbacks_pipe -lpthread
```
## Run the callbacks 
Start xpm10 group 0 timing by running groupca:
```
groupca DAQ:NEH 10 0
```
Run the program
```
./user_callbacks_pipe
...
(daq_20241215) monarin@drp-neh-cmp012 debug cat cb_dld_event.out | head -n 100
configuration source used: inifile configuration with [tdc_gpx3.ini] as parameter
Output Format
 total bits len:64
 channel off:62
 channel len:2
 index_ch pos:0
 time data off:0
 time data len:0
 time tag off:0
 time tag len:0
 start counter off:49
 start counter len:13
 sign counter off:0
 sign counter len:0
 dif1 off:0
 dif1 len:12
 dif2 off:12
 dif2 len:12
 sum off:24
 sum len:25
 flow flags:0
00-------000000ab
01-------00620620
02-------00062004
03-------00000000
04-------02000000
05-------0b0009b4
06-------08000000
07-------00001fb4
10-------00000000
11-------04000000
12-------00000800
16-------000000ab
17-------00620620
18-------00062004
19-------00000000
20-------02000000
21-------0b0009b4
22-------08000000
23-------00001fb4
26-------00000000
27-------04000000
28-------00000800
StartCounter = 8559	FreezedTimer = 11828
AutoStartPeriod = 7144242	AutoModulo = 228615729
StartPeriod = 0	Modulo = 0
ROI: 32768 - 32767	32768 - 32767	0 - -1
START cn_measures: 0
DLDEVENT: 1
  j: 0 timetag: 13532 (0.13532) sum: 123309 dif1: 683 dif2: 579
  j: 1 timetag: 9223380949233448338 (2147485723.321533330) sum: 16918265 dif1: 912 dif2: 993
  j: 2 timetag: 9223380949233448429 (2147485723.321533421) sum: 8465184 dif1: 1823 dif2: 810
  j: 3 timetag: 9223380949233448793 (2147485723.321533785) sum: 8530370 dif1: 1003 dif2: 1038
DLDEVENT: 2
  j: 0 timetag: 9223380949233449248 (2147485723.321534240) sum: 151409 dif1: 1688 dif2: 2313
  j: 1 timetag: 9223380949233449339 (2147485723.321534331) sum: 25322183 dif1: 136 dif2: 1676
  j: 2 timetag: 9223380949233449612 (2147485723.321534604) sum: 150621 dif1: 1183 dif2: 673
  j: 3 timetag: 9223380949233449612 (2147485723.321534604) sum: 160054 dif1: 1022 dif2: 354
  j: 4 timetag: 9223380949233449612 (2147485723.321534604) sum: 165416 dif1: 2163 dif2: 36
  j: 5 timetag: 9223380949233449703 (2147485723.321534695) sum: 25320140 dif1: 0 dif2: 264
  j: 6 timetag: 9223380949233449794 (2147485723.321534786) sum: 16906937 dif1: 2141 dif2: 1266
  j: 7 timetag: 9223380949233449885 (2147485723.321534877) sum: 8510719 dif1: 182 dif2: 401
  j: 8 timetag: 9223380949233449976 (2147485723.321534968) sum: 126160 dif1: 1094 dif2: 1538
DLDEVENT: 3
  j: 0 timetag: 9223380949233450431 (2147485723.321535423) sum: 25317836 dif1: 1368 dif2: 2221
  j: 1 timetag: 9223380949233450522 (2147485723.321535514) sum: 16926901 dif1: 2323 dif2: 1082
  j: 2 timetag: 9223380949233450795 (2147485723.321535787) sum: 25227762 dif1: 683 dif2: 1492
  j: 3 timetag: 9223380949233450795 (2147485723.321535787) sum: 25323809 dif1: 1322 dif2: 1173
DLDEVENT: 4
  j: 0 timetag: 9223380949233451068 (2147485723.321536060) sum: 158807 dif1: 1686 dif2: 856
  j: 1 timetag: 9223380949233451159 (2147485723.321536151) sum: 25300791 dif1: 2370 dif2: 218
  j: 2 timetag: 9223380949233451159 (2147485723.321536151) sum: 25311362 dif1: 2505 dif2: 901
  j: 3 timetag: 9223380949233451250 (2147485723.321536242) sum: 16928996 dif1: 2230 dif2: 1628
  j: 4 timetag: 9223380949233451341 (2147485723.321536333) sum: 8544979 dif1: 1914 dif2: 1904
  j: 5 timetag: 9223380949233451432 (2147485723.321536424) sum: 128880 dif1: 272 dif2: 2313
  j: 6 timetag: 9223380949233451614 (2147485723.321536606) sum: 16834302 dif1: 2255 dif2: 1539
  j: 7 timetag: 9223380949233451705 (2147485723.321536697) sum: 8540364 dif1: 92 dif2: 2405
DLDEVENT: 5
  j: 0 timetag: 9223380949233451887 (2147485723.321536879) sum: 25316367 dif1: 1230 dif2: 1266
  j: 1 timetag: 9223380949233452069 (2147485723.321537061) sum: 8453933 dif1: 866 dif2: 307
  j: 2 timetag: 9223380949233452160 (2147485723.321537152) sum: 146993 dif1: 501 dif2: 1172
  j: 3 timetag: 9223380949233452160 (2147485723.321537152) sum: 164845 dif1: 228 dif2: 1404
  j: 4 timetag: 9223380949233452433 (2147485723.321537425) sum: 8521114 dif1: 182 dif2: 80
  j: 5 timetag: 9223380949233452706 (2147485723.321537698) sum: 16922958 dif1: 2095 dif2: 263
```
## Understanding the cb_dld_event callback
Setting: measurement range: 1000ms
```
groupca       no. of        no. of e-
rate (Hz)  cb_dld_events
  1              1           1 or 2
  10             4           1 or 2
  100            44          1-3  
```
