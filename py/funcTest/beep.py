import time
import lgpio

print("0-gpio_ver: ", lgpio.get_module_version())

curPin = 20
gpio_chipId = 4

h = lgpio.gpiochip_open(gpio_chipId)
print("1-open handle =", h, "  GPIO pin: ", curPin)

r = lgpio.gpio_claim_output(h, curPin)
print("  ret of gpio_claim_output is: ", r)

Times = 0

try:
    print("loop ...")
    while True:
        r = lgpio.gpio_write(h, curPin, 1)
        print("  times-{:>03} | write gpio:{}   ret={}".format(Times, curPin, r))
        time.sleep(0.2)
        
        lgpio.gpio_write(h, curPin, 0)
        time.sleep(0.8)
        Times += 1
        
except KeyboardInterrupt:
    lgpio.gpio_write(h, curPin, 0)
    lgpio.gpiochip_close(h)
    
