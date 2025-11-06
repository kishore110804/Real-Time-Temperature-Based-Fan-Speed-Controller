/**
 * SIMPLIFIED VERSION FOR RENODE SIMULATION
 * Bare-metal temperature control demo without complex HAL
 * This version WILL work in Renode!
 */

#include <stdint.h>
#include <stdio.h>

// Memory-mapped register addresses for STM32F103
#define RCC_BASE        0x40021000
#define RCC_APB2ENR     (*(volatile uint32_t *)(RCC_BASE + 0x18))
#define RCC_APB1ENR     (*(volatile uint32_t *)(RCC_BASE + 0x1C))

#define GPIOA_BASE      0x40010800
#define GPIOA_CRL       (*(volatile uint32_t *)(GPIOA_BASE + 0x00))
#define GPIOA_CRH       (*(volatile uint32_t *)(GPIOA_BASE + 0x04))
#define GPIOA_ODR       (*(volatile uint32_t *)(GPIOA_BASE + 0x0C))

#define USART1_BASE     0x40013800
#define USART1_SR       (*(volatile uint32_t *)(USART1_BASE + 0x00))
#define USART1_DR       (*(volatile uint32_t *)(USART1_BASE + 0x04))
#define USART1_BRR      (*(volatile uint32_t *)(USART1_BASE + 0x08))
#define USART1_CR1      (*(volatile uint32_t *)(USART1_BASE + 0x0C))

// Simple delay function
void delay_ms(uint32_t ms) {
    for(uint32_t i = 0; i < ms * 1000; i++) {
        __asm__("nop");
    }
}

// Simple UART transmit
void uart_send_char(char c) {
    while(!(USART1_SR & (1 << 7)));  // Wait for TXE
    USART1_DR = c;
}

void uart_send_string(const char *str) {
    while(*str) {
        uart_send_char(*str++);
    }
}

// Simple integer to string conversion
void int_to_string(int num, char *buf) {
    if(num == 0) {
        buf[0] = '0';
        buf[1] = '\0';
        return;
    }
    
    int i = 0;
    int temp = num;
    
    if(num < 0) {
        buf[i++] = '-';
        num = -num;
    }
    
    // Count digits
    int digits = 0;
    temp = num;
    while(temp > 0) {
        digits++;
        temp /= 10;
    }
    
    // Convert
    i += digits;
    buf[i] = '\0';
    while(num > 0) {
        buf[--i] = '0' + (num % 10);
        num /= 10;
    }
}

// Simple GPIO and UART initialization
void init_peripherals(void) {
    // Enable clocks: GPIOA, USART1
    RCC_APB2ENR |= (1 << 2);  // GPIOA
    RCC_APB2ENR |= (1 << 14); // USART1
    
    // Configure PA9 as TX (Alternate function push-pull)
    GPIOA_CRH &= ~(0xF << 4);  // Clear PA9 config
    GPIOA_CRH |= (0xB << 4);   // PA9: Alt func push-pull, 50MHz
    
    // Configure PA10 as RX (Input floating)
    GPIOA_CRH &= ~(0xF << 8);  // Clear PA10 config
    GPIOA_CRH |= (0x4 << 8);   // PA10: Input floating
    
    // Configure USART1: 115200 baud @ 8MHz
    USART1_BRR = 69;  // 8MHz / 115200 ≈ 69
    USART1_CR1 = (1 << 13) | (1 << 3) | (1 << 2); // UE, TE, RE
}

int main(void) {
    // Initialize peripherals
    init_peripherals();
    
    // Send startup message
    uart_send_string("\r\n========================================\r\n");
    uart_send_string("STM32 Fan Control Simulation\r\n");
    uart_send_string("========================================\r\n\r\n");
    
    // Simulated temperature and PWM values
    uint16_t adc_value = 310;  // Start at 25°C
    uint16_t pwm_duty = 0;
    int temperature = 25;
    char buffer[50];
    int cycle = 0;
    
    while(1) {
        // Calculate PWM from temperature (proportional control)
        // PWM range: 0-4000, Temp range: 0-100°C
        pwm_duty = (temperature * 40);
        if(pwm_duty > 4000) pwm_duty = 4000;
        
        // Calculate ADC value from temperature
        // LM35: 10mV/°C, so 25°C = 0.25V
        // ADC 12-bit: 0.25V / 3.3V * 4095 ≈ 12.4 * temperature
        adc_value = temperature * 12;
        
        // Send formatted output
        uart_send_string("Temp: ");
        int_to_string(temperature, buffer);
        uart_send_string(buffer);
        uart_send_string(" C | ADC: ");
        int_to_string(adc_value, buffer);
        uart_send_string(buffer);
        uart_send_string(" | PWM: ");
        int_to_string(pwm_duty, buffer);
        uart_send_string(buffer);
        uart_send_string(" | Fan: ");
        int_to_string((pwm_duty * 100) / 4000, buffer);
        uart_send_string(buffer);
        uart_send_string("%\r\n");
        
        // Simulate temperature increase every 10 cycles (5 seconds)
        cycle++;
        if(cycle >= 10) {
            cycle = 0;
            temperature += 5;
            if(temperature > 100) temperature = 25; // Wrap around
        }
        
        delay_ms(500);
    }
    
    return 0;
}
