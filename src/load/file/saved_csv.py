def save_cleaned(df, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"{len(df)} rows saved to {output_file}")
