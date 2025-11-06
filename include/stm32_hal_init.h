/**
 * ============================================================
 * STM32F103C8 HAL Initialization Header
 * ============================================================
 */

#ifndef STM32_HAL_INIT_H
#define STM32_HAL_INIT_H

#include <stdint.h>

/* ============================================================
 * System Initialization
 * ============================================================ */

/**
 * Configure system clock (72 MHz from 8 MHz HSE)
 */
void SystemClock_Config(void);

/**
 * Initialize GPIO pins
 * - PA0: ADC input (analog)
 * - PA6: PWM output (TIM3_CH1)
 * - PA9: UART TX
 * - PA10: UART RX
 */
void GPIO_Init(void);

/* ============================================================
 * Peripheral Initialization
 * ============================================================ */

/**
 * Initialize ADC1 on PA0 (12-bit, single conversion)
 */
void ADC1_Init(void);

/**
 * Initialize TIM3 PWM on PA6 (8 kHz, 0-1125 range)
 */
void TIM3_PWM_Init(void);

/**
 * Initialize UART1 (115200 baud, 8N1)
 */
void UART1_Init(void);

/* ============================================================
 * Peripheral Driver Functions
 * ============================================================ */

/**
 * Read ADC value from temperature sensor
 * 
 * Returns: ADC count (0-4095)
 */
uint16_t ADC_Read_Temperature(void);

/**
 * Set PWM duty cycle
 * 
 * Parameters:
 *   duty_cycle: 0-1125 (0% to 100%)
 */
void PWM_Set_Duty(uint16_t duty_cycle);

/**
 * Convert ADC reading to temperature
 * 
 * Parameters:
 *   adc_value: 0-4095
 *   
 * Returns: Temperature in °C (0-100°C range)
 */
float ADC_To_Temperature(uint16_t adc_value);

/**
 * Calculate PWM duty cycle from temperature
 * 
 * Parameters:
 *   temperature: Temperature in °C
 *   
 * Returns: PWM duty cycle (0-1125)
 * 
 * Control curve:
 *   - < 25°C: 0% (off)
 *   - 25-45°C: Linear ramp
 *   - > 45°C: 100% (full speed)
 */
uint16_t Temperature_To_PWM(float temperature);

/**
 * Send string via UART1
 * 
 * Parameters:
 *   str: Null-terminated string
 */
void UART_SendString(const char *str);

/**
 * Error handler (infinite loop)
 */
void Error_Handler(void);

#endif /* STM32_HAL_INIT_H */
