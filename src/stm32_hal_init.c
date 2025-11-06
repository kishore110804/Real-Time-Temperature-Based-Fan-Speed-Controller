/**
 * ============================================================
 * STM32F103C8 HAL Initialization Functions
 * ============================================================
 * 
 * ADC1:  PA0 (Temperature sensor input)
 * TIM3:  PA6 (PWM output for fan control)
 * UART1: PA9 (TX), PA10 (RX) - 115200 baud
 * 
 * Compiler: STM32CubeMX HAL Library
 * MCU: STM32F103C8 (BluePill)
 */

#include "stm32f1xx_hal.h"
#include "stm32_hal_init.h"

/* ============================================================
 * GLOBAL HANDLES
 * ============================================================ */

ADC_HandleTypeDef hadc1;
TIM_HandleTypeDef htim3;
UART_HandleTypeDef huart1;

/* ============================================================
 * SYSTEM CLOCK CONFIGURATION
 * ============================================================
 * 
 * Clock Configuration:
 * - HSE: 8 MHz (external crystal)
 * - PLL: ×9 = 72 MHz
 * - AHB: 72 MHz
 * - APB1: 36 MHz
 * - APB2: 72 MHz
 */

void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    /* STM32F1 does not have voltage scaling - removed */
    __HAL_RCC_PWR_CLK_ENABLE();

    /* USE HSI FOR RENODE SIMULATION - HSE doesn't work well in emulation */
    /* DISABLE PLL TO AVOID WAIT LOOPS - just use HSI directly (8MHz) */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;  // NO PLL for simulation

    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
    {
        Error_Handler();
    }

    /* Initializes the CPU, AHB and APB bus clocks */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                  | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;  // Use HSI directly, no PLL
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;    // 8MHz
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;     // 8MHz
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;     // 8MHz

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
    {
        Error_Handler();
    }
}

/* ============================================================
 * GPIO INITIALIZATION
 * ============================================================
 * 
 * PA0:  Analog input (ADC1_IN0) - Temperature sensor
 * PA6:  Alternate function (TIM3_CH1) - PWM output
 * PA9:  Alternate function (USART1_TX)
 * PA10: Input floating (USART1_RX)
 */

void GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /* Configure PA0 - ADC Input (Analog) */
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* Configure PA6 - PWM Output (TIM3_CH1) */
    GPIO_InitStruct.Pin = GPIO_PIN_6;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* Configure PA9 - UART1 TX */
    GPIO_InitStruct.Pin = GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* Configure PA10 - UART1 RX */
    GPIO_InitStruct.Pin = GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/* ============================================================
 * ADC1 INITIALIZATION
 * ============================================================
 * 
 * Channel: PA0 (ADC1_IN0)
 * Resolution: 12-bit
 * Sampling time: 239.5 cycles
 * Mode: Single conversion
 */

void ADC1_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};

    /* ADC1 Clock Enable */
    __HAL_RCC_ADC1_CLK_ENABLE();

    /* ADC1 Configuration */
    hadc1.Instance = ADC1;
    hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;

    if (HAL_ADC_Init(&hadc1) != HAL_OK)
    {
        Error_Handler();
    }

    /* Configure ADC Channel - PA0 (Channel 0) */
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = ADC_REGULAR_RANK_1;
    sConfig.SamplingTime = ADC_SAMPLETIME_239CYCLES_5;

    if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
    {
        Error_Handler();
    }

    /* ADC Calibration */
    if (HAL_ADCEx_Calibration_Start(&hadc1) != HAL_OK)
    {
        Error_Handler();
    }
}

/* ============================================================
 * TIM3 PWM INITIALIZATION
 * ============================================================
 * 
 * Channel: CH1 (PA6)
 * Frequency: 8 kHz
 * Prescaler: 8 (72MHz / 8 = 9MHz)
 * Period: 1125 (9MHz / 1125 = 8kHz)
 * PWM Range: 0-1125 (0-100%)
 */

void TIM3_PWM_Init(void)
{
    TIM_OC_InitTypeDef sConfigOC = {0};

    /* TIM3 Clock Enable */
    __HAL_RCC_TIM3_CLK_ENABLE();

    /* TIM3 Configuration */
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 8 - 1;           /* Divide 72MHz by 8 = 9MHz */
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 1125 - 1;           /* 9MHz / 1125 = 8kHz */
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.RepetitionCounter = 0;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

    if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
    {
        Error_Handler();
    }

    /* Configure PWM Channel 1 (PA6) */
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 0;                    /* Initial duty cycle: 0% */
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

    if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
    {
        Error_Handler();
    }

    /* Start PWM Generation */
    if (HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1) != HAL_OK)
    {
        Error_Handler();
    }
}

/* ============================================================
 * UART1 INITIALIZATION
 * ============================================================
 * 
 * Baudrate: 115200
 * Data bits: 8
 * Stop bits: 1
 * Parity: None
 * Flow control: None
 */

void UART1_Init(void)
{
    /* UART1 Clock Enable */
    __HAL_RCC_USART1_CLK_ENABLE();

    /* UART1 Configuration */
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;

    if (HAL_UART_Init(&huart1) != HAL_OK)
    {
        Error_Handler();
    }
}

/* ============================================================
 * PERIPHERAL DRIVER FUNCTIONS
 * ============================================================ */

/**
 * Read ADC value from PA0 (Temperature sensor)
 * 
 * Returns: ADC count (0-4095)
 * Voltage range: 0-3.3V
 * Temperature: 0-100°C (LM35: 10mV/°C)
 */
uint16_t ADC_Read_Temperature(void)
{
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
    uint16_t adc_value = HAL_ADC_GetValue(&hadc1);
    HAL_ADC_Stop(&hadc1);
    return adc_value;
}

/**
 * Set PWM duty cycle on PA6 (Fan speed control)
 * 
 * Parameters:
 *   duty_cycle: 0-1125 (0% to 100%)
 *   
 * Typical usage:
 *   0 = Motor off
 *   563 = 50% speed
 *   1125 = 100% speed
 */
void PWM_Set_Duty(uint16_t duty_cycle)
{
    if (duty_cycle > 1125)
        duty_cycle = 1125;  /* Limit to max */

    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, duty_cycle);
}

/**
 * Convert ADC reading to temperature in °C
 * 
 * LM35 characteristics:
 *   - 10mV per °C
 *   - 0°C = 0V
 *   - 100°C = 1V
 *   - ADC range: 0-4095 = 0-3.3V
 *   
 * Formula: Temperature = (ADC * 3.3 / 4095) / 0.01
 */
float ADC_To_Temperature(uint16_t adc_value)
{
    float voltage = (float)adc_value * 3.3f / 4095.0f;
    float temperature = voltage / 0.01f;  /* LM35: 10mV/°C */
    return temperature;
}

/**
 * Calculate PWM duty cycle based on temperature
 * 
 * Control curve:
 *   - Temp < 25°C: Motor off
 *   - 25-45°C: Linear ramp (0% to 100%)
 *   - Temp > 45°C: Motor full speed
 */
uint16_t Temperature_To_PWM(float temperature)
{
    if (temperature < 25.0f)
        return 0;                           /* Motor off */
    
    if (temperature > 45.0f)
        return 1125;                        /* Full speed */
    
    /* Linear interpolation: 25°C → 0%, 45°C → 100% */
    float ratio = (temperature - 25.0f) / (45.0f - 25.0f);
    return (uint16_t)(ratio * 1125.0f);
}

/**
 * UART Transmit string
 * 
 * Useful for debugging and monitoring
 */
void UART_SendString(const char *str)
{
    uint16_t len = 0;
    while (str[len] != '\0')
        len++;

    HAL_UART_Transmit(&huart1, (uint8_t *)str, len, HAL_MAX_DELAY);
}

/**
 * Error Handler
 * Called if any HAL initialization fails
 */
void Error_Handler(void)
{
    /* Infinite loop - indicates initialization error */
    while (1)
    {
        /* Add LED blink or debug output here */
    }
}

/* ============================================================
 * MAIN APPLICATION LOOP
 * ============================================================
 * 
 * Call from main():
 * 
 * int main(void)
 * {
 *     HAL_Init();
 *     SystemClock_Config();
 *     GPIO_Init();
 *     ADC1_Init();
 *     TIM3_PWM_Init();
 *     UART1_Init();
 *
 *     while (1)
 *     {
 *         uint16_t adc_value = ADC_Read_Temperature();
 *         float temperature = ADC_To_Temperature(adc_value);
 *         uint16_t pwm_duty = Temperature_To_PWM(temperature);
 *         PWM_Set_Duty(pwm_duty);
 *         
 *         // Optional: Send debug data via UART
 *         // HAL_Delay(500);
 *     }
 *
 *     return 0;
 * }
 */
