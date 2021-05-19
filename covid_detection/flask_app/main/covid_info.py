from covid import Covid
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
plt.style.use('fivethirtyeight')
#%matplotlib inline

covid = Covid()
covid1 = Covid(source="worldometers")


def get_world_total_count():
    active = covid.get_total_active_cases()
    confirmed = covid.get_total_confirmed_cases()
    recovered = covid.get_total_recovered()
    deaths = covid.get_total_deaths()
    total_cnts = {'ACTIVE' : active, 'CONFIRMED': confirmed, 'DEATHS': deaths, 'RECOVERED': recovered}
    return total_cnts

def get_country_list():
    #covid_info = covid.get_data()
    '''countries_id = covid.list_countries()
    countries = list()
    for i in countries_id:
        countries.append(i['name'])
    return countries  '''
    #cntry_list = covid1.list_countries()#for dropdown
    #final_cntry_list = [i.capitalize() for i in cntry_list if i.strip() != '']
    final_cntry_list=confirmed_df['Country/Region'].unique().tolist()
    return final_cntry_list




def get_countrywise_total_count(country='India'):
    country_status = covid.get_status_by_country_name(country)
    rem_list = ['id','latitude','longitude','last_update']
    [country_status.pop(key, None) for key in rem_list]
    return country_status
    
#print(get_countrywise_total_count())
dir_path = 'D:\\My_study_for_data_science\\python\\covid_detection\\covid_detection\\covid_detection\\flask_app\\static\\'

daily_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-15-2021.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
cols = confirmed_df.keys()
confirmed = confirmed_df.loc[:, cols[4]:cols[-1]]
deaths = death_df.loc[:, cols[4]:cols[-1]]
recovered = recovered_df.loc[:, cols[4]:cols[-1]]

# Creating pie plot
def draw_pie_diagram(data,labels,cols,title,path):
    print('Inside draw_pie')
    fig = plt.figure(figsize =(10, 7))
    my_explode = (0.1, 0, 0, 0, 0 ,0)
    plt.pie(data, labels = labels,autopct='%1.1f%%', startangle=50, shadow = True,explode=my_explode)
    plt.title(title+ 'Date (mm/dd/yy): '+ cols[-1])
    plt.axis('equal')
    #plt.show()
    print(path)
    plt.savefig(path)

# creating the bar plot
def draw_bar_diagram(x,y,title,path):
    fig = plt.figure(figsize = (12, 8))    
    plt.bar(x,y, color ='orange',width = 0.4)   
    plt.xlabel("Countries")
    plt.ylabel("Corona cases")
    plt.title(title+ 'Date (mm/dd/yy): '+ cols[-1])
    print(path)
    plt.savefig(path)

## Get top 5 affected countries comparison    
def getDiagram_top5_corona_affected_cnty_comparison(dia='pie'):
    print('inside dia')
    World_total_recent_confirmed = confirmed_df[cols[-1]].sum()
    World_total_recent_death = death_df[cols[-1]].sum()
    World_total_recent_recovered = recovered_df[cols[-1]].sum()

    top_five_recent_confirmed = confirmed_df.sort_values(cols[-1],ascending=False).head()[[cols[1],cols[-1]]]
    top_five_recent_confirmed
    other_cnt = int(World_total_recent_confirmed) - int(top_five_recent_confirmed.sum().to_list()[1])
    top_five_recent_confirmed.loc[len(top_five_recent_confirmed.index)] = ['Others',other_cnt] 

    top_five_recent_deaths = death_df.sort_values(cols[-1],ascending=False).head()[[cols[1],cols[-1]]]
    other_cnt_death = int(World_total_recent_death) - int(top_five_recent_deaths.sum().to_list()[1])
    top_five_recent_deaths.loc[len(top_five_recent_deaths.index)] = ['Others',other_cnt_death] 

    top_five_recent_recovered = recovered_df.sort_values(cols[-1],ascending=False).head()[[cols[1],cols[-1]]]
    other_cnt_recovered = int(World_total_recent_recovered) - int(top_five_recent_recovered.sum().to_list()[1])
    top_five_recent_recovered.loc[len(top_five_recent_recovered.index)] = ['Others',other_cnt_recovered]   
  
    dia_names = []
    if(dia == 'pie'):
        draw_pie_diagram(top_five_recent_confirmed[cols[-1]],top_five_recent_confirmed[cols[1]],cols,'Confirmed Corona cases worldwide',dir_path+'top_five_recent_confirmed_pie.png')
        draw_pie_diagram(top_five_recent_deaths[cols[-1]],top_five_recent_deaths[cols[1]],cols,'Deaths due to Corona cases worldwide',dir_path+'top_five_recent_deaths_pie.png')
        draw_pie_diagram(top_five_recent_recovered[cols[-1]],top_five_recent_recovered[cols[1]],cols,'Recovered Corona cases worldwide',dir_path+'top_five_recent_recovered_pie.png')
        dia_names=['top_five_recent_confirmed_pie.png','top_five_recent_deaths_pie.png','top_five_recent_recovered_pie.png']
    elif(dia == 'bar'):
        draw_bar_diagram(top_five_recent_confirmed[cols[1]].iloc[:5], top_five_recent_confirmed[cols[-1]].iloc[:5],'Corona cases comparison among top 5 countries',dir_path+'top_five_recent_confirmed_bar.png')
        draw_bar_diagram(top_five_recent_deaths[cols[1]].iloc[:5], top_five_recent_deaths[cols[-1]].iloc[:5],'Corona cases death comparison among top 5 countries',dir_path+'top_five_recent_deaths_bar.png')
        draw_bar_diagram(top_five_recent_recovered[cols[1]].iloc[:5], top_five_recent_recovered[cols[-1]].iloc[:5],'Corona cases recovered comparison among top 5 countries',dir_path+'top_five_recent_recovered_bar.png')
        dia_names=['top_five_recent_confirmed_bar.png','top_five_recent_deaths_bar.png','top_five_recent_recovered_bar.png']
    return dia_names

def draw_line_plot(dates,data1,data2,data3,country,path):
    plt.figure(figsize= (15,10))
    plt.xticks(rotation = 90 ,fontsize = 11)
    plt.yticks(fontsize = 10)
    plt.xlabel("Dates",fontsize = 20)
    plt.ylabel('Total cases',fontsize = 20)
    plt.title("Total Confirmed, Active, Death in "+ country , fontsize = 20)

    ax1 = plt.plot_date(y= data1,x= dates,label = 'Confirmed',linestyle ='-',color = 'b')
    ax2 = plt.plot_date(y= data2,x= dates,label = 'Recovered',linestyle ='-',color = 'g')
    ax3 = plt.plot_date(y= data3,x= dates,label = 'Death',linestyle ='-',color = 'r')
    plt.legend()
    plt.savefig(path)




def getDiagram_Country_analysis(country):
    india_confirmed=confirmed_df.loc[confirmed_df['Country/Region']==country].iloc[:,4:]
    india_deaths=death_df.loc[death_df['Country/Region']==country].iloc[:,4:]
    india_recovered=recovered_df.loc[recovered_df['Country/Region']==country].iloc[:,4:]

    dates = list(confirmed_df.columns[4:])
    dates = list(pd.to_datetime(dates))
    dia_name = country+'_analysis.png'
    draw_line_plot(dates,india_confirmed.iloc[0],india_recovered.iloc[0],india_deaths.iloc[0],country,dir_path+dia_name)
    return dia_name

def getRateAnalysis():# we can get old data as well
    dates = confirmed.keys()
    world_cases = []
    total_deaths = [] 
    mortality_rate = []
    total_active = []
    total_recovered = []
    recovery_rate = []

    for i in dates:
        confirmed_sum = confirmed[i].sum()
        death_sum = deaths[i].sum()
        recovered_sum = recovered[i].sum()
        
        # confirmed, deaths, recovered, and active
        world_cases.append(confirmed_sum)
        total_deaths.append(death_sum)
        total_recovered.append(recovered_sum)
        total_active.append(confirmed_sum-death_sum-recovered_sum)
        
        # calculate rates
        mortality_rate.append(death_sum/confirmed_sum)
        recovery_rate.append(recovered_sum/confirmed_sum)

    print(world_cases[-5:])


#getDiagram_Country_analysis('China')
#getDiagram_top5_corona_affected_cnty_comparison('bar')

