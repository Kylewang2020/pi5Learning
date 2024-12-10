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


def gpio_close(chip, pin_in, pin_out):
    '''lgpio 终止'''
    lgpio.gpio_free(chip, pin_in)
    lgpio.gpio_write(chip, pin_out, 0)
    lgpio.gpio_free(chip, pin_out)
    lgpio.gpiochip_close(chip)
    print(" gpio_close:   done")


def voice_detect(event, chip, pin_in, pin_out):
    '''使用 lgpio 库模拟 PWM函数'''
    # 设置 GPIO 引脚为 输入
    r = lgpio.gpio_claim_input(chip, pin_in)
    print(" voice_detect: set GPIO-{} to output {}".format(pin_out, "成功" if r>=0 else "失败!"))
    
    # 设置 GPIO 引脚为输出
    r = lgpio.gpio_claim_output(chip, pin_out)
    print(" voice_detect: set GPIO-{} to output {}".format(pin_out, "成功" if r>=0 else "失败!"))

    try:
        while not event.is_set():  # 检查事件是否被设置
            value = lgpio.gpio_read(chip, pin_in)
            if value == 0:
                print(f"GPIO {pin_in} 低电平")
                # 输出高电平
                lgpio.gpio_write(chip, pin_out, 1)
            else:
                # 输出低电平
                lgpio.gpio_write(chip, pin_out, 0)
                # print(f"GPIO {pin_in} 高电平")
            time.sleep(0.1)
        print(" voice_detect: event发生接收到, PWM函数退出")
        
    except KeyboardInterrupt:
        print(" voice_detect: 键盘终止 PWM函数退出")


# 主函数
def main():
    # 参数设置 
    pin_in = 5
    pin_out = 21
    gpiochip = 4

    chip = gpio_init(gpiochip)

    try:
        stop_event = threading.Event()      # 创建一个 Event 对象，用于安全退出
        thread = threading.Thread(target=voice_detect, args=(stop_event, chip, pin_in, pin_out))
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
        gpio_close(chip, pin_in, pin_out)
        print(" main: 退出程序")
        
if __name__ == "__main__":
    main()
