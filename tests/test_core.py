from wifiaudit.core import wifi_inventory


def test_wifi_inventory_returns_platform_and_task():
    report = wifi_inventory()
    assert "platform" in report
    assert report["task"] == "wifi_inventory"
