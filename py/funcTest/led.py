
import time
import lgpio

def PWM(chip, pin, frequency, duty_cycle):
    '''使用 lgpio 库模拟 PWM函数'''
    # 计算周期（秒）
    period = 1 / frequency
    high_time = period * (duty_cycle / 100)  # 高电平持续时间
    low_time = period - high_time  # 低电平持续时间
    # 模拟 PWM 输出
    try:
        # 配置 GPIO pin 为输出
        lgpio.gpio_claim_output(chip, pin)        
        while True:
            # 输出高电平
            lgpio.gpio_write(chip, pin, 1)
            time.sleep(high_time)
            # 输出低电平
            lgpio.gpio_write(chip, pin, 0)
            time.sleep(low_time)
    except KeyboardInterrupt:
        print("键盘终止 PWM函数退出")


print("0-gpio_ver: ", lgpio.get_module_version())
gpio_chipId = 4
curPin = 21

# 打开 GPIO 芯片 4 (当前我的 GPIO 芯片的编号 为4)
chip = lgpio.gpiochip_open(gpio_chipId)
print("1-open handle =", chip, "  GPIO pin: ", curPin)

# 设置 GPIO 引脚为输出
r = lgpio.gpio_claim_output(chip, curPin)
print("  ret of gpio_claim_output is: ", r)

# 设置 GPIO 引脚为输入
# lgpio.gpio_claim_input(chip, 18)  # 假设你要使用 GPIO 18 作为输入

Times = 0
TimesSpan = 0.01


try:
    print("loop ...")
    PWM(chip, curPin, 1000, 50)
    # lgpio.gpio_write(chip, curPin, 1)
    # while True:
        # lgpio.gpio_write(chip, curPin, 1)
        # time.sleep(0.5*TimesSpan)
        # lgpio.gpio_write(chip, curPin, 0)
        # time.sleep(0.5*TimesSpan)
        # time.sleep(0.5)
        
except KeyboardInterrupt:
    print("键盘终止 主函数退出")

finally:    
    lgpio.gpio_write(chip, curPin, 0)
    lgpio.gpio_free(chip, curPin)
    lgpio.gpiochip_close(chip)
    print("退出程序")
    
