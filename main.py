import pandas as pd
import matplotlib.pyplot as plt

def main(): 
    df = pd.read_csv(   # ograniczam do dwóch parametrów + timestamp 
        "data/raw/MetroPT3(AirCompressor).csv",
        usecols=["timestamp", "Oil_temperature", "Motor_current"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df[    # ograniczam zakres dat -> wg dokumentacji cały miesiąc czysty 
        (df["timestamp"] >= "2020-02-01") &
        (df["timestamp"] <= "2020-03-01")
    ]
    df = df.sort_values('timestamp').reset_index(drop=True)  #sortowanie 
    df['dt'] = df['timestamp'].diff().dt.total_seconds()
    print(df[['Motor_current', 'Oil_temperature']].describe()) #sprawdzam czy są błędy pomiarowe 

    #sprawdzanie czy nie ma dziur w timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])   # sprawdzenie formatu
    df = df.sort_values('timestamp').reset_index(drop=True) # sortowane
    df['dt'] = df['timestamp'].diff().dt.total_seconds()    # różnice czasowe pomiędzy próbkami
  

    print('Różnice czasowe:')
    print(df['dt'].describe())

#   Wizualizacja - szukam odchyłek do wycięcia    
    # # plt.figure(figsize=(14, 4))
    # # plt.plot(df['timestamp'], df['Motor_current'], label='Motor current')
    # # plt.legend()
    # # plt.show()
    # plt.figure(figsize=(14, 4))
    # plt.plot(df['timestamp'], df['Oil_temperature'], label='Oil_temperature')
    # plt.legend()
    # plt.show()

    df_clean = df.copy() 
    df_clean['is_off'] = df_clean['Motor_current'] < 0.5    # silnik off
    df_clean['is_cold_start'] = df_clean['Oil_temperature'] < 35    # zimny olej
    print(df_clean[['is_off', 'is_cold_start']].mean())



if __name__ == "__main__":
    main()