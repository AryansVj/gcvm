#include <windows.h>
#include <stdio.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Devices.Bluetooth.GenericAttributeProfile.h>
#pragma comment(lib, "windowsapp")

using namespace winrt;
using namespace Windows::Devices::Bluetooth::GenericAttributeProfile;
using namespace Windows::Devices::Enumeration;
using namespace Windows::Foundation;

void TemperatureValueChanged(
    GattCharacteristic sender,
    GattValueChangedEventArgs args)
{
    // Handle the received temperature value
    auto reader = DataReader::FromBuffer(args.CharacteristicValue());
    int32_t temperatureValue = reader.ReadInt32();

    printf("Temperature: %d°C\n", temperatureValue);
}

int main()
{
    init_apartment();

    const wchar_t* htsServiceUuid = L"00001809-0000-1000-8000-00805f9b34fb";
    const wchar_t* temperatureCharUuid = L"00002a1c-0000-1000-8000-00805f9b34fb";

    // Find HTS service devices
    auto selector = GattDeviceService::GetDeviceSelectorFromUuid(GUID{});
    auto services = DeviceInformation::FindAllAsync(selector).get();

    if (services.Size() == 0)
    {
        printf("HTS service not found.\n");
        return 0;
    }

    // Connect to the first available HTS service
    auto service = GattDeviceService::FromIdAsync(services.GetAt(0).Id()).get();

    // Get the temperature characteristic
    auto characteristics = service.GetCharacteristicsAsync().get();
    GattCharacteristic temperatureChar{ nullptr };

    for (auto&& characteristic : characteristics)
    {
        if (characteristic.Uuid().ToString() == temperatureCharUuid)
        {
            temperatureChar = characteristic;
            break;
        }
    }

    if (!temperatureChar)
    {
        printf("Temperature characteristic not found.\n");
        return 0;
    }

    // Subscribe to notifications
    temperatureChar.ValueChanged(TemperatureValueChanged);
    temperatureChar.WriteClientCharacteristicConfigurationDescriptorAsync(
        GattClientCharacteristicConfigurationDescriptorValue::Notify).get();

    printf("Connected to the HTS service.\n");

    // Keep the program running
    getchar();

    return 0;
}
