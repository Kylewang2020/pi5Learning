# 树莓派5

## 40引脚GPIO定义

>树莓派5的GPIO引脚定义与之前的树莓派4基本一致，采用了40个引脚，其中包含GPIO、供电、地线和一些专用功能引脚。这些引脚通过BCM（Broadcom）编号系统来标识，而不是物理位置编号。以下是树莓派5的40个引脚定义：

| 引脚编号 (Physical Pin) | BCM编号 | 功能/描述                      |
|-------------------------|---------|-------------------------------|
| 1                       | -       | 3.3V 电源 (Power)              |
| 2                       | -       | 5V 电源 (Power)                |
| 3                       | 2       | SDA (I2C Data)                 |
| 4                       | -       | 5V 电源 (Power)                |
| 5                       | 3       | SCL (I2C Clock)                |
| 6                       | -       | GND (Ground)                   |
| 7                       | 4       | GPIO 4                          |
| 8                       | 14      | TXD (UART Transmit)            |
| 9                       | -       | GND (Ground)                   |
| 10                      | 15      | RXD (UART Receive)             |
| 11                      | 17      | GPIO 17                         |
| 12                      | 18      | GPIO 18 (PWM)                  |
| 13                      | 27      | GPIO 27                         |
| 14                      | -       | GND (Ground)                   |
| 15                      | 22      | GPIO 22                         |
| 16                      | 23      | GPIO 23                         |
| 17                      | -       | 3.3V 电源 (Power)              |
| 18                      | 24      | GPIO 24                         |
| 19                      | 10      | MOSI (SPI Data Out)            |
| 20                      | -       | GND (Ground)                   |
| 21                      | 9       | MISO (SPI Data In)             |
| 22                      | 25      | GPIO 25                         |
| 23                      | 11      | SCLK (SPI Clock)               |
| 24                      | 8       | CE0 (SPI Chip Select 0)        |
| 25                      | -       | GND (Ground)                   |
| 26                      | 7       | CE1 (SPI Chip Select 1)        |
| 27                      | 0       | ID_SD (I2C EEPROM)             |
| 28                      | 1       | ID_SC (I2C EEPROM)             |
| 29                      | 5       | GPIO 5                          |
| 30                      | -       | GND (Ground)                   |
| 31                      | 6       | GPIO 6                          |
| 32                      | 12      | GPIO 12 (PWM)                  |
| 33                      | 13      | GPIO 13 (PWM)                  |
| 34                      | -       | GND (Ground)                   |
| 35                      | 19      | GPIO 19 (SPI MISO)             |
| 36                      | 16      | GPIO 16                         |
| 37                      | 26      | GPIO 26                         |
| 38                      | 20      | GPIO 20                         |
| 39                      | -       | GND (Ground)                   |
| 40                      | 21      | GPIO 21                         |

## 引脚功能概述

### 电源引脚：

- Pin 1: 3.3V 电源
- Pin 2: 5V 电源
- Pin 4: 5V 电源
- Pin 17: 3.3V 电源
- Pin 6, 9, 14, 20, 25, 30, 34, 39: 地线 (GND)

### GPIO 引脚：

- 这些引脚可以用来作为输入、输出、PWM（脉宽调制）等多种功能的配置，具体引脚可以参考上表。
- 例如，GPIO 2（Pin 3）和GPIO 3（Pin 5）是I2C总线的SDA和SCL信号线，GPIO 14（Pin 8）和GPIO 15（Pin 10）是UART串口通信的TX和RX。

### I2C、SPI、UART接口：

- I2C： 
SDA和SCL分别连接到GPIO 2和GPIO 3。
- SPI： 
SPI总线上的MOSI、MISO、SCLK和CE引脚分别连接到GPIO 10、GPIO 9、GPIO 11和GPIO 8（CE0）。GPIO 7（Pin 26）是SPI的CE1引脚。
- UART： TXD（GPIO 14）和RXD（GPIO 15）用于串口通信。

- PWM输出：
GPIO 18（Pin 12）和GPIO 13（Pin 33）等可以用来生成PWM信号，用于调节电机、LED亮度等。

### 使用GPIO的注意事项

- 电流限制：每个GPIO引脚的最大输出电流通常是16mA，总的最大电流不超过50mA，因此建议通过外部电路（如使用晶体管或继电器）来驱动高功率设备。
- 电压保护：GPIO引脚只能承受3.3V电压，输入电压超过此值可能会损坏树莓派，因此接入外部电压时要确保电压适配。

### GPIO编程

可以使用多种编程语言（如Python、C、C++等）来控制GPIO。例如，使用Python的RPi.GPIO库或gpiozero库来控制GPIO引脚。

通过上述引脚定义，你可以根据需要进行GPIO的配置和应用开发。