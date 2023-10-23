## RIX Mono Encoder/ Trigger
- mono_enc_trig only sets up a low-rate “tpr” trigger to the hardware.  
- mono_encoder_0 is the real daq process that receives the low-rate udp packets from the encoder, and interpolates between them to higher rates
- mono_encoder_0 runs at the high rate

drp-srcf-cmp002
[mono_encoder]
