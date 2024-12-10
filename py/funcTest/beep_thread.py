import threading
import time
import lgpio


def gpio_init(gpiochip):
    '''lgpio 初始化'''
    print(" gpio_init:   gpio_ver=", lgpio.get_module_version())
    # 打开 GPIO 芯片 4 (当前我的 GPIO 芯片的编号 为4)
    chip = lgpio.gpiochip_open(gpiochip)
    print(" gpio_init:   handle =", chip)
    return chip


def gpio_close(chip, pin):
    '''lgpio 终止'''
    lgpio.gpio_write(chip, pin, 0)
    lgpio.gpio_free(chip, pin)
    lgpio.gpiochip_close(chip)
    print(" gpio_close:   done")


def PWM(event, chip, pin, frequency, duty_cycle):
    '''使用 lgpio 库模拟 PWM函数'''
    # 设置 GPIO 引脚为输出
    r = lgpio.gpio_claim_output(chip, pin)
    print(" PWM: set GPIO-{} to output {}".format(pin, "成功" if r>=0 else "失败!"))

    # 计算周期（秒）
    period = 1 / frequency
    high_time = period * (duty_cycle / 100)  # 高电平持续时间
    low_time = period - high_time  # 低电平持续时间
    print(" PWM: set frequency={}; period={:.3f}s; duty_cycle={:.2f}%; high_time={:.5f}s".format(
        frequency, period, duty_cycle, high_time))

    try:
        while not event.is_set():  # 检查事件是否被设置
            # 输出高电平
            lgpio.gpio_write(chip, pin, 1)
            time.sleep(high_time)
            # 输出低电平
            lgpio.gpio_write(chip, pin, 0)
            time.sleep(low_time)
        print(" PWM: stop event发生, PWM函数退出")
        lgpio.gpio_write(chip, pin, 0)
    except KeyboardInterrupt:
        print(" PWM: 键盘终止 PWM函数退出")


# 主函数
def main():
    # 参数设置
    curPin = 20
    gpiochip = 4
    frequency = 0.5
    duty_cycle = 50
    
    chip = gpio_init(gpiochip)
    
    try:
        stop_event = threading.Event()      # 创建一个 Event 对象，用于安全退出
        thread = threading.Thread(target=PWM, args=(stop_event, chip, curPin, frequency, duty_cycle))
        thread.daemon = True  # 设置为守护线程
        thread.start()

        print(" main: loop start...")
        while not stop_event.is_set():  # 检查事件是否被设置
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        # 设置停止事件，通知所有线程退出
        print(" main: 键盘终止 主线程通知所有线程退出...")
        stop_event.set()

    finally:
        thread.join()
        gpio_close(chip, curPin)
        print(" main: 退出程序")
        
if __name__ == "__main__":
    main()
