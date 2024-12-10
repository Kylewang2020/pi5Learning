import time
import lgpio

Led = 23

print("0-gpio_ver: ", lgpio.get_module_version())

h = lgpio.gpiochip_open(0)
print("1-open:      h=", h)
lgpio.gpio_claim_output(h, Led)

Times = 0

try:
    print("loop ...")
    while True:
        print("  times: ", Times)
        lgpio.gpio_write(h, Led, 1)
        time.sleep(1)
        
        # lgpio.gpio_write(h, Led, 0)
        time.sleep(1)
        Times += 1
        
except KeyboardInterrupt:
    lgpio.gpio_write(h, Led, 0)
    lgpio.gpiochip_close(h)
    
