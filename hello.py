from datetime import datetime

def get_greeting(name="Claude"):
    return {
        "message": f"Hello from {name}!",
        "time": f"{datetime.now():%Y-%m-%d %H:%M:%S}",
    }

def main():
    greeting = get_greeting()
    print(greeting["message"])
    print(f"Current time: {greeting['time']}")

if __name__ == "__main__":
    main()
