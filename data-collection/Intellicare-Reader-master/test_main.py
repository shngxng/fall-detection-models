from main import load_configuration

def test_load_configuration():
    filename = "test_config_default.conf"
    config = load_configuration(filename)
    assert config['target'] == "0"
    assert config['csv_file_name'].startswith("output_")

    filename = "test_config_with_values.conf"
    config = load_configuration(filename)
    assert config['target'] == "1"
    assert config['csv_file_name'] == "test.csv"


print("RUN Test Load Configuration")
test_load_configuration()
print("PASSED")