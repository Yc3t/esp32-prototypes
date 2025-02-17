#include <stdio.h>
#include <string.h>
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "esp_log.h"

static const char *TAG = "BLE_SCAN";

static esp_ble_scan_params_t ble_scan_params = {
    .scan_type              = BLE_SCAN_TYPE_ACTIVE,
    .own_addr_type         = BLE_ADDR_TYPE_PUBLIC,
    .scan_filter_policy    = BLE_SCAN_FILTER_ALLOW_ALL,
    .scan_interval         = 0x50,
    .scan_window           = 0x30,
    .scan_duplicate        = BLE_SCAN_DUPLICATE_DISABLE
};

static void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param)
{
    switch (event) {
        case ESP_GAP_BLE_SCAN_PARAM_SET_COMPLETE_EVT:
            esp_ble_gap_start_scanning(0); // Scan continuously
            break;
            
        case ESP_GAP_BLE_SCAN_START_COMPLETE_EVT:
            if (param->scan_start_cmpl.status != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(TAG, "Scan start failed");
            }
            break;

        case ESP_GAP_BLE_SCAN_RESULT_EVT:
            if (param->scan_rst.search_evt == ESP_GAP_SEARCH_INQ_RES_EVT) {
                // Print device address
                printf("Device address: ");
                for (int i = 0; i < 6; i++) {
                    printf("%02X", param->scan_rst.bda[i]);
                    if (i < 5) printf(":");
                }
                printf("\n");

                // Print RSSI
                printf("RSSI: %d\n", param->scan_rst.rssi);

                // Print device name if available
                if (param->scan_rst.adv_data_len > 0) {
                    uint8_t *adv_data = param->scan_rst.ble_adv;
                    uint8_t adv_data_len = param->scan_rst.adv_data_len;
                    uint8_t scan_data_len = param->scan_rst.scan_rsp_len;
                    
                    // Parse advertisement data
                    for (int i = 0; i < adv_data_len; ) {
                        uint8_t length = adv_data[i];
                        uint8_t type = adv_data[i + 1];
                        
                        // Look for device name
                        if (type == ESP_BLE_AD_TYPE_NAME_CMPL || type == ESP_BLE_AD_TYPE_NAME_SHORT) {
                            printf("Device name: ");
                            for (int j = 0; j < length - 1; j++) {
                                printf("%c", adv_data[i + 2 + j]);
                            }
                            printf("\n");
                        }
                        i += length + 1;
                    }
                }
                printf("------------------------\n");
            }
            break;

        default:
            break;
    }
}

void app_main(void)
{
    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize BT controller and stack
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_bt_controller_init(&bt_cfg));
    ESP_ERROR_CHECK(esp_bt_controller_enable(ESP_BT_MODE_BLE));
    ESP_ERROR_CHECK(esp_bluedroid_init());
    ESP_ERROR_CHECK(esp_bluedroid_enable());

    // Register callback function
    ESP_ERROR_CHECK(esp_ble_gap_register_callback(esp_gap_cb));

    // Set scan parameters
    ESP_ERROR_CHECK(esp_ble_gap_set_scan_params(&ble_scan_params));

    printf("BLE Scan started...\n");
}