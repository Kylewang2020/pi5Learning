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
    # lgpio.gpio_free(chip, pin_in)
    lgpio.gpio_write(chip, pin_out, 0)
    lgpio.gpio_free(chip, pin_out)
    lgpio.gpiochip_close(chip)
    print(" gpio_close:   done")


def get_duty_cycle(angle):
    '''依据角度计算sg90的占空比'''
    speed = 0.002 # 速度约为 0.12 秒/60度，即0.002 秒/度
    if angle>=360: 
        sg_angle = angle - 360
    elif angle>180: 
        sg_angle = angle-180
    else:
        sg_angle = angle
    duty_cycle = (sg_angle/45.0)*2.5 + 2.5
    wait_time = speed*180+0.2
    print("角度:{}, sg角度:{}, duty_cycle:{}%, wait_time{}s".format(
        angle, sg_angle, duty_cycle, wait_time))
    return duty_cycle, wait_time
  
    
def PWM(chip, pin, angle, frequency=50):
    '''使用 lgpio 库模拟 PWM函数'''
    
    duty_cycle, wait_time = get_duty_cycle(angle)
    
    # 设置 GPIO 引脚为输出
    r = lgpio.gpio_claim_output(chip, pin)
    print(" PWM: set GPIO-{} to output {}".format(pin, "成功" if r>=0 else "失败!"))

    # 计算周期（秒）
    period = 1 / frequency
    high_time = period * (duty_cycle / 100)  # 高电平持续时间
    low_time = period - high_time  # 低电平持续时间
    print(" PWM: set frequency={}; period={:.3f}ms; duty_cycle={:.2f}%; high_time={:.5f}ms".format(
        frequency, period*1000, duty_cycle, high_time*1000))

    try:
        runTime = 0.0
        while True:
            # 输出高电平
            lgpio.gpio_write(chip, pin, 1)
            time.sleep(high_time)
            # 输出低电平
            lgpio.gpio_write(chip, pin, 0)
            time.sleep(low_time)
            runTime += period
            if runTime > wait_time: break
        print(" PWM: PWM函数退出")
        lgpio.gpio_write(chip, pin, 0)
    except KeyboardInterrupt:
        print(" PWM: 键盘终止 PWM函数退出")


# 主函数
def main():
    # 参数设置 
    gpiochip = 4
    pin_in = 5
    pin_out = 18
    frequency = 50 # 周期20ms
    span = 0.02
    high_time = 0.5*0.001   # 0度
    # high_time = 1*0.001     # 45度
    # high_time = 1.25*0.001     # 77.5度
    # high_time = 1.5*0.001   # 90度
    # high_time = 2.0*0.001   # 135度
    # high_time = 2.5*0.001   # 180度
    
    chip = gpio_init(gpiochip)
    lgpio.gpio_claim_output(chip, pin_out)

    run_time = 1
    PWM(chip, pin_out, 180)
    try:
        print(" main: loop ...")
        # while True:
        #     # print("  run_time: ", run_time)
        #     lgpio.gpio_write(chip, pin_out, 1)
        #     time.sleep(high_time)
            
        #     lgpio.gpio_write(chip, pin_out, 0)
        #     time.sleep(span-high_time)
        #     run_time += 1
        #     # time.sleep(span*10)
        #     if run_time*span>0.5: break
        # print(" main: loop end")
    except KeyboardInterrupt:
        print(" main: 键盘终止 主线程通知所有线程退出...")

    finally:
        gpio_close(chip, pin_in, pin_out)
        print(" main: 退出程序")
    

if __name__ == "__main__":
    main()
    # for angle in [0, 45, 75, 90, 135, 180]:
    #     print("角度:{}, 占空比:{}".format(angle, get_duty_cycle(angle)))
