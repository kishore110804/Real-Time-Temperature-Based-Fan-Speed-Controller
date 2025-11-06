/**
 * SIMULATION-FRIENDLY VERSION - Uses HSI instead of HSE
 * This version works with Renode which doesn't fully emulate external crystals
 */

#include "stm32f1xx_hal.h"

void SystemClock_Config_Sim(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    /* Use HSI (Internal 8MHz RC oscillator) for simulation */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI_DIV2;  // HSI/2 = 4MHz
    RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL16;              // 4MHz × 16 = 64MHz

    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
    {
        /* Initialization Error - but in simulation, continue anyway */
    }

    /* Configure CPU, AHB and APB clocks */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                  | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;    // 64MHz
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;     // 32MHz
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;     // 64MHz

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
    {
        /* Configuration Error - but in simulation, continue anyway */
    }
}
