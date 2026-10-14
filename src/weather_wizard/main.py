from weather_wizard.core.weather_wizard import WeatherWizard

def main():
    print("Attempting to run main...")
    try:
        wizard = WeatherWizard()
        wizard.run()
    except Exception as e:
        print(f"failed to start: {str(e)}")

if __name__ == "__main__":
    main()