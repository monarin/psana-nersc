## user_callbacks_pipe
From documentation.pdf page 34, we can supply different callbacks to the start (cb_start), receving event (cb_dld_event), and end (cb_end) phases. Below shows a modified version:
```
#include <stdio.h>
#include <stdlib.h>
#include <scTDC.h>
#include <inttypes.h>
struct sc_DeviceProperties3 sizes;

struct PrivData {
    int event_count;
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
    priv_data->event_count++;
    printf("START event_count: %d, total_time: %f\n", priv_data->event_count, priv_data->total_time);
}
void cb_end(void *p) {
    /* this function gets called every time a measurement finishes */
    struct PrivData *priv_data = (struct PrivData *)p; 
    printf("END event_count: %d, total_time: %f\n", priv_data->event_count, priv_data->total_time);
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
    printf("TDCEVENT event_count: %d, total_time: %f\n", priv_data->event_count, priv_data->total_time);
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
    printf("DLDEVENT event_count: %d, total_time: %f\n", priv_data->event_count, priv_data->total_time);
    const char *buffer = (const char *) event_array;
    size_t j;
    for (j=0; j<event_array_len; ++j) {
        const struct sc_DldEvent *obj =
            (const struct sc_DldEvent *)(buffer + j * sizes.tdc_event_size);
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
        printf("  j: %d start_counter: %llu timetag: %llu dif1: %hu dif2: %hu\n", j, start_counter, time_tag, dif1, dif2);

    }
}

int main()
{
    int dd;
    int ret;
    struct PrivData priv_data = {0, 0.0};
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
DLDEVENT event_count: 1, total_time: 0.000000
  j: 0 start_counter: 0 timetag: 0 dif1: 956 dif2: 1313
  j: 1 start_counter: 0 timetag: 0 dif1: 12060 dif2: 2
  j: 2 start_counter: 2361482 timetag: 0 dif1: 0 dif2: 0
  j: 3 start_counter: 157165 timetag: 100926761 dif1: 0 dif2: 0
  j: 4 start_counter: 0 timetag: 159882 dif1: 0 dif2: 0
  j: 5 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 6 start_counter: 0 timetag: 0 dif1: 2414 dif2: 1538
  j: 7 start_counter: 0 timetag: 0 dif1: 34400 dif2: 2
  j: 8 start_counter: 53215687 timetag: 0 dif1: 0 dif2: 0
  j: 9 start_counter: 147212 timetag: 148703234 dif1: 0 dif2: 0
  j: 10 start_counter: 0 timetag: 157596 dif1: 0 dif2: 0
  j: 11 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 12 start_counter: 0 timetag: 0 dif1: 773 dif2: 720
  j: 13 start_counter: 0 timetag: 0 dif1: 54746 dif2: 0
  j: 14 start_counter: 47055759 timetag: 0 dif1: 0 dif2: 0
  j: 15 start_counter: 63490 timetag: 100861907 dif1: 0 dif2: 0
  j: 16 start_counter: 0 timetag: 135277 dif1: 0 dif2: 0
  j: 17 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 18 start_counter: 0 timetag: 0 dif1: 409 dif2: 1630
  j: 19 start_counter: 0 timetag: 0 dif1: 852 dif2: 2
  j: 20 start_counter: 41223784 timetag: 0 dif1: 0 dif2: 0
  j: 21 start_counter: 168870 timetag: 68027234 dif1: 0 dif2: 0
  j: 22 start_counter: 0 timetag: 152078 dif1: 0 dif2: 0
  j: 23 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 24 start_counter: 0 timetag: 0 dif1: 92 dif2: 355
  j: 25 start_counter: 0 timetag: 0 dif1: 26590 dif2: 2
  j: 26 start_counter: 118817905 timetag: 0 dif1: 0 dif2: 0
  j: 27 start_counter: 152364 timetag: 127796019 dif1: 0 dif2: 0
  j: 28 start_counter: 0 timetag: 158730 dif1: 0 dif2: 0
  j: 29 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 30 start_counter: 0 timetag: 0 dif1: 1822 dif2: 1038
  j: 31 start_counter: 0 timetag: 0 dif1: 62151 dif2: 1
  j: 32 start_counter: 50135176 timetag: 0 dif1: 0 dif2: 0
  j: 33 start_counter: 147334 timetag: 136708370 dif1: 0 dif2: 0
  j: 34 start_counter: 0 timetag: 146580 dif1: 0 dif2: 0
  j: 35 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 36 start_counter: 0 timetag: 0 dif1: 1870 dif2: 1676
  j: 37 start_counter: 0 timetag: 0 dif1: 6173 dif2: 2
  j: 38 start_counter: 17368815 timetag: 0 dif1: 0 dif2: 0
  j: 39 start_counter: 157228 timetag: 38209536 dif1: 0 dif2: 0
  j: 40 start_counter: 0 timetag: 145003 dif1: 0 dif2: 0
  j: 41 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 42 start_counter: 0 timetag: 0 dif1: 638 dif2: 1768
  j: 43 start_counter: 0 timetag: 0 dif1: 30789 dif2: 2
  j: 44 start_counter: 94896356 timetag: 0 dif1: 0 dif2: 0
  j: 45 start_counter: 151472 timetag: 83034386 dif1: 0 dif2: 0
  j: 46 start_counter: 0 timetag: 160008 dif1: 0 dif2: 0
  j: 47 start_counter: 0 timetag: 0 dif1: 0 dif2: 0
  j: 48 start_counter: 0 timetag: 0 dif1: 819 dif2: 128
END event_count: 1, total_time: 0.000000
```
