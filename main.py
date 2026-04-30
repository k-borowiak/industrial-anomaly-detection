import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def main(): 
    cols = ["timestamp", "Oil_temperature", "Motor_current"]
    df = pd.read_csv(   # ograniczam do dwóch parametrów + timestamp 
        "data/raw/MetroPT3(AirCompressor).csv",
        usecols=cols,
        parse_dates=["timestamp"]
    )
    df = df.sort_values("timestamp").reset_index(drop=True) #sortowanie wg czasu

    df_base = df[                           # wycięcie timestamp -> 01.02 - 11.03 
    (df["timestamp"] >= "2020-02-01") &
    (df["timestamp"] <= "2020-03-05")
    ].copy()
   
    time_diff = df_base["timestamp"].diff()

    df_base["new_segment"] = time_diff > pd.Timedelta("1 hour")
    df_base["segment_id"] = df_base["new_segment"].cumsum()

    print(df_base[['Motor_current', 'Oil_temperature']].describe().round(3)) #sprawdzam czy są błędy pomiarowe 

    scaler = StandardScaler()

    df_base[["Oil_temperature", "Motor_current"]] = scaler.fit_transform(
    df_base[["Oil_temperature", "Motor_current"]]
    )
    print(df_base[['Motor_current', 'Oil_temperature']].describe().round(3)) #sprawdzam czy są błędy pomiarowe 

    fig, axes = plt.subplots(2, 1, figsize=(16, 6), sharex=True)

    axes[0].plot(df_base["timestamp"], df_base["Oil_temperature"], linewidth=0.5)
    axes[0].set_title("Oil Temperature")
    axes[0].set_ylabel("Oil Temperature")

    axes[1].plot(df_base["timestamp"], df_base["Motor_current"], linewidth=0.5)
    axes[1].set_title("Motor Current")
    axes[1].set_ylabel("Motor Current")
    axes[1].set_xlabel("Time")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()