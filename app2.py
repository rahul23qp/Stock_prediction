from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg') 
import seaborn as sns
import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch stock data
    model = load_model('Stock.h5')
    tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
    end = datetime.now()
    start = datetime(end.year - 1, end.month, end.day)

    for stock in tech_list:
        globals()[stock] = yf.download(stock, start, end)
        
    company_list = [AAPL, GOOG, MSFT, AMZN]
    company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]

    for company, com_name in zip(company_list, company_name):
        company["company_name"] = com_name
        
    df = pd.concat(company_list, axis=0)

    # Prepare data columns
    # data_columns = {}
    # for company, name in zip(company_list, company_name):
    #     data_columns[name] = company[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Plotting the historical view of the closing price
    plt.figure(figsize=(15, 10))
    plt.subplots_adjust(top=1.25, bottom=1.2)

    for i, company in enumerate(company_list, 1):
        plt.subplot(2, 2, i)
        company['Adj Close'].plot()
        plt.ylabel('Adj Close')
        plt.xlabel(None)
        plt.title(f"Closing Price of {tech_list[i - 1]}")
        
    plt.tight_layout()
    closing_price_plot_path = 'static/closing_price.png'
    plt.savefig(closing_price_plot_path)
    
    # Plotting the total volume of stock being traded each day
    plt.figure(figsize=(15, 10))
    plt.subplots_adjust(top=1.25, bottom=1.2)

    for i, company in enumerate(company_list, 1):
        plt.subplot(2, 2, i)
        company['Volume'].plot()
        plt.ylabel('Volume')
        plt.xlabel(None)
        plt.title(f"Sales Volume for {tech_list[i - 1]}")
        
    plt.tight_layout()
    sales_volume_plot_path = 'static/sales_volume.png'
    plt.savefig(sales_volume_plot_path)
    
    # Plotting the moving averages
    ma_day = [10, 20, 50]

    for ma in ma_day:
        for company in company_list:
            column_name = f"MA for {ma} days"
            company[column_name] = company['Adj Close'].rolling(ma).mean()
            
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figheight(10)
    fig.set_figwidth(15)

    AAPL[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[0,0])
    axes[0,0].set_title('APPLE')

    GOOG[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[0,1])
    axes[0,1].set_title('GOOGLE')

    MSFT[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[1,0])
    axes[1,0].set_title('MICROSOFT')

    AMZN[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[1,1])
    axes[1,1].set_title('AMAZON')

    fig.tight_layout()
    moving_average_plot_path = 'static/moving_average.png'
    plt.savefig(moving_average_plot_path)
    
    # Plotting the daily return percentage
    for company in company_list:
        company['Daily Return'] = company['Adj Close'].pct_change()
    # Plot daily return for each company
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

    for i, (company, name) in enumerate(zip(company_list, company_name), 1):
        row = (i - 1) // 2
        col = (i - 1) % 2
        company['Daily Return'].plot(ax=axes[row, col], legend=True, linestyle='--', marker='o')
        axes[row, col].set_title(name)

    fig.tight_layout()

# Save the plot
    daily_return_plot_path = 'static/daily_return.png'
    plt.savefig(daily_return_plot_path)
    
    # Rendering the template with all the plot images
    return render_template('index.html',
                           closing_price_plot=closing_price_plot_path,
                           sales_volume_plot=sales_volume_plot_path,
                           moving_average_plot=moving_average_plot_path,
                           daily_return_plot=daily_return_plot_path)

if __name__ == '__main__':
    app.run(debug=True)
