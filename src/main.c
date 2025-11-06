#include "main.h"
#include "stm32f1xx_hal.h"
#include "stm32_hal_init.h"  // Include our HAL initialization functions

ADC_HandleTypeDef hadc1;
TIM_HandleTypeDef htim3;
UART_HandleTypeDef huart1;

void send_uart(char *str) {
    HAL_UART_Transmit(&huart1, (uint8_t*)str, strlen(str), 100);
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    GPIO_Init();
    ADC1_Init();
    TIM3_PWM_Init();
    UART1_Init();

    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
    uint32_t adc_val = 0;
    float temperature = 0;
    char buffer[50];

    while (1) {
        // ====== Task 1: Read Temperature ======
        HAL_ADC_Start(&hadc1);
        HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
        adc_val = HAL_ADC_GetValue(&hadc1);
        HAL_ADC_Stop(&hadc1);

        temperature = (adc_val * 3.3 / 4095) * 100; // LM35 scale (10mV/°C)

        // ====== Task 2: Control Fan (PWM Duty) ======
        uint16_t pwm = (uint16_t)(temperature * 40); // scale 0–4000
        if (pwm > 4000) pwm = 4000;
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, pwm);

        // ====== Task 3: UART Log ======
        sprintf(buffer, "Temp: %.2f C, PWM: %d\r\n", temperature, pwm);
        send_uart(buffer);

        HAL_Delay(500);  // For RMS: 500 ms periodic task
    }
}

/* Note: SystemClock_Config, MX_ADC1_Init, MX_TIM3_Init, MX_USART1_UART_Init, 
   and MX_GPIO_Init are now implemented in stm32_hal_init.c */
