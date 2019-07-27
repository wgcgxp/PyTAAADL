import os
import numpy as np
import datetime
import pandas

_cwd = os.getcwd()
#os.chdir(os.path.dirname(__file__))
from functions.allstats import allstats
from functions.GetParams import GetParams
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
os.chdir(_cwd)

def avg_DD(x, periods):
    DD = np.zeros_like(np.array(x))
    maxx = x[0]
    for i in range(1, len(DD)):
        maxx = max(maxx, x[i])
        DD[i] = (x[i] - maxx) / maxx
    return DD[-periods:].mean()

# --------------------------------------------------
# Get program parameters.
# --------------------------------------------------

run_params = GetParams()

# --------------------------------------------------
# set filename for datafram containing model persistence input data.
# --------------------------------------------------

datearray_new_months = [datetime.date(1997, 1, 2)]
#persistence_hdf = os.path.join(_cwd,'pngs','best_performers4','persistence_data_2-9.hdf')
#persistence_hdf = os.path.join(_cwd,'pngs','best_performers4','persistence_data_full.hdf')
#persistence_hdf = os.path.join(_cwd,'pngs','best_performers5','persistence_data_full_v3.hdf')
#persistence_hdf = os.path.join(_cwd,'pngs',run_params['folder_for_best_performers'],run_params['persistence_hdf'])

#_performance_folder, persistence_hdf_fn = os.path.split(persistence_hdf)
#_persistence_filename_prefix = os.path.splitext(persistence_hdf_fn)[0]

persistence_hdf = os.path.join(_cwd,'pngs',run_params['folder_for_best_performers'],run_params['persistence_hdf'])
_performance_folder, persistence_hdf_fn = os.path.split(persistence_hdf)
_persistence_filename_prefix = os.path.splitext(persistence_hdf_fn)[0]

df3 = pandas.HDFStore(persistence_hdf).select('table')

df3_array = df3.as_matrix()
df3_array_labels = np.array(df3.columns)
datearray_new_months = [df3_array[-1][0]]

# --------------------------------------------------
# create csv fie for output comparison.
# --------------------------------------------------

performance_text = "evaluation date" + "," + \
                   "sorting choices" + "," + \
                   "number stocks choices" + "," + \
                   "persistence months" + "," + \
                   "final value" + "," + \
                   "persistence_DD" + "," + \
                   "persistence_mid_DD" + "," + \
                   "persistence_recent_DD" + "," + \
                   "persistence_sortinos" + "," + \
                   "persistence_mid_sortinos" + "," + \
                   "persistence_recent_sortinos" + "," + \
                   "persistence_sharpes" + "," + \
                   "persistence_mid_sharpes" + "," + \
                   "persistence_recent_sharpes" + "\n"

csv_file = os.path.join(_performance_folder, 'PyTAAADL_dynamic_persistence.csv')
with open(csv_file, 'w') as f:
    f.write(performance_text)

# --------------------------------------------------
# loop to test different combinations of persistence.
# --------------------------------------------------

persistence_values = []
persistence_number_stocks_choices = []
persistence_sorting_choices = []
unique_id_list = []
final_values = []
persistence_series_values = []
persistence_sortinos = []
persistence_mid_sortinos = []
persistence_recent_sortinos = []
persistence_sharpes = []
persistence_mid_sharpes = []
persistence_recent_sharpes = []
persistence_DD = []
persistence_mid_DD = []
persistence_recent_DD = []
#persistence_months_list = range(6,20)
persistence_months_list = [3,4,5,6,8,10,12,15,18]
number_stocks_choices = [[2,7],[2,4,7],[2,5,7,9],[2,3,4,5,6,7,8,9],[2,5,6,7,8],[3,5,7,9],[2,4,6,8]]
#number_stocks_choices = [[2,7],[2,5,7],[2,5,7,9],[2,4,5,6,7,8,9],[2,5,6,7,8],[5,7,9],[2,4,6,8]]
sorting_choices = [['sortino','sharpe','count','equal'],
                   ['sortino','count','equal'],
                   ['sortino','count'],
                   ['count'],
                   ['sortino','sharpe','count']]

#persistence_months_list = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#number_stocks_choices = [[3,5,7,9]]
#sorting_choices = [['sortino','sharpe','count','equal']]

for inum_sort_choice in sorting_choices:
    for inum_stocks_choices in number_stocks_choices:
        df5 = pandas.DataFrame(columns=['dates', 'sort_modes', 'number_stocks', 'gains', 'symbols', 'weights', 'cumu_value'])
        if persistence_hdf_fn == 'persistence_data_2-9.hdf' or persistence_hdf_fn == 'persistence_data_full_v3.hdf':
            for i,idate in enumerate(df3.values[:,0]):
                datarow=list(df3.values[i])
                #datarow.insert(0, idate)
                #print(i,df3.values[i,1])
                if i%1000==0:
                    print("...progress... ",i)
                if df3.values[i,2] in inum_stocks_choices and df3.values[i,1] in inum_sort_choice:
                    df5.loc[len(df5)] = datarow
        elif persistence_hdf_fn == 'persistence_data_full.hdf':
            for i,idate in enumerate(df3.index):
                datarow=list(df3.values[i])
                datarow.insert(0, idate)
                #print(i,df3.values[i,1])
                if i%1000==0:
                    print("...progress... ",i)
                if df3.values[i,1] in inum_stocks_choices and df3.values[i,0] in inum_sort_choice:
                    df5.loc[len(df5)] = datarow
        else:
            icount = 0
            for i, idate in enumerate(df3.index):
                datarow = df3.iloc[[i]]
                if i%1000==0:
                    print("...progress... ",i)
                #if datarow['number_stocks'].values[0] in inum_stocks_choices:
                #    print(datarow['number_stocks'].values[0], datarow['number_stocks'].values[0] in inum_stocks_choices, datarow['sort_modes'].values[0], datarow['sort_modes'].values[0] in inum_sort_choice)
                if datarow['number_stocks'].values[0] in inum_stocks_choices and datarow['sort_modes'].values[0] in inum_sort_choice:
                    icount += 1
                    df5 = df5.append(datarow, ignore_index=True)

        print("df5 shape = ",df5.values.shape)

        # generate (unique) lists with unique values for number_stocks, sort_modes, and dates
        _dates = df5.values[:,0]
        _number_stocks = df5.values[:,2]
        _sort_mode = df5.values[:,1]
        dates_list = list(set(_dates))
        number_stocks_list = list(set(_number_stocks))
        sort_mode_list = list(set(_sort_mode))
        dates_list.sort()
        number_stocks_list.sort()
        sort_mode_list.sort()

        for persistence_months in persistence_months_list:

            # how many months of persistence should be used to indicate 'best'?
            print("\n\n\n ... persistence_months = ", persistence_months, " ...\n\n")
            from time import sleep
            sleep(5)

            cumu_dynamic_system = [10000.0]
            plotdates = [datearray_new_months[0]]

            recent_comparative_gain = [1.]
            recent_comparative_month_gain = [1.]
            recent_comparative_method = ['cash']
            recent_comparative_nstocks = [0]

            for i, idate in enumerate(dates_list):

                recent_comparative_gain = [1.]
                recent_comparative_month_gain = [1.]
                recent_comparative_method = ['cash']
                recent_comparative_nstocks = [0]

                for inum_stocks in number_stocks_list:
                    for sort_mode in sort_mode_list:

                        indices = df5.loc[np.logical_and(df5['sort_modes']==sort_mode,df5['number_stocks']==inum_stocks)]['gains'].index
                        dates_for_selected = df5.values[indices,0]
                        cumugains_for_selected = 10000.*(df5.values[indices,-4]+1.).cumprod()
                        idate_index = np.argmin(np.abs(dates_for_selected - idate))
                        method_cumu_gains = cumugains_for_selected[:idate_index+1]

                        try:
                            recent_comparative_gain.append(method_cumu_gains[-2]/method_cumu_gains[-persistence_months-2])
                            recent_comparative_month_gain.append(method_cumu_gains[-1]/method_cumu_gains[-2])
                            recent_comparative_method.append(sort_mode)
                            recent_comparative_nstocks.append(inum_stocks)
                        except:
                            recent_comparative_gain.append(1.)
                            recent_comparative_month_gain.append(1.)
                            recent_comparative_method.append('cash')
                            recent_comparative_nstocks.append(0)

                        if sort_mode == sort_mode_list[-1] and inum_stocks == number_stocks_list[-1]:
                            plotdates.append(idate)
                            best_comparative_index = np.argmax(recent_comparative_gain)
                            cumu_dynamic_system.append(cumu_dynamic_system[-1] * recent_comparative_month_gain[best_comparative_index])
                            '''
                            print("        ... methods, near-term gains ",
                                  str(idate), recent_comparative_method,
                                  np.around(recent_comparative_gain,2))
                            '''
                            print("        ... dynamic system = ", str(idate),
                                  recent_comparative_nstocks[best_comparative_index],
                                  recent_comparative_method[best_comparative_index],
                                  format(cumu_dynamic_system[-1], '10,.0f'))

            persistence_sorting_choices.append(inum_sort_choice)
            persistence_number_stocks_choices.append(inum_stocks_choices)
            persistence_values.append(persistence_months)
            final_values.append(cumu_dynamic_system[-1])
            persistence_series_values.append(cumu_dynamic_system)
            persistence_DD.append(avg_DD(np.array(cumu_dynamic_system),len(cumu_dynamic_system)))
            persistence_mid_DD.append(avg_DD(np.array(cumu_dynamic_system),int(12*11.75)))
            persistence_recent_DD.append(avg_DD(np.array(cumu_dynamic_system),int(12*4.75)))
            try:
                persistence_sortinos.append(allstats(np.array(cumu_dynamic_system)).sortino())
            except:
                persistence_sortinos.append(0.)
            try:
                persistence_mid_sortinos.append(allstats(np.array(cumu_dynamic_system[-int(12*11.75):])).sortino())
            except:
                persistence_mid_sortinos.append(0.)
            try:
                persistence_recent_sortinos.append(allstats(np.array(cumu_dynamic_system[-int(12*4.75):])).sortino())
            except:
                persistence_recent_sortinos.append(0.)
            try:
                persistence_sharpes.append(allstats(np.array(cumu_dynamic_system)).monthly_sharpe())
            except:
                persistence_sharpes.append(0.)
            try:
                persistence_mid_sharpes.append(allstats(np.array(cumu_dynamic_system[-int(12*11.75):])).monthly_sharpe())
            except:
                persistence_mid_sharpes.append(0.)
            try:
                persistence_recent_sharpes.append(allstats(np.array(cumu_dynamic_system[-int(12*4.75):])).monthly_sharpe())
            except:
                persistence_recent_sharpes.append(0.)

            unique_id = format(persistence_months,'03d')+" "+str(inum_stocks_choices)+str(inum_sort_choice)
            unique_id_list.append(unique_id)

            if persistence_months == persistence_months_list[0] and inum_stocks_choices == number_stocks_choices[0] and inum_sort_choice == sorting_choices[0]:
                plt.close(1)
                plt.figure(1)
                plt.yscale('log')
                plt.grid(True)
            if persistence_months==18:
                plt.plot(plotdates, cumu_dynamic_system, 'k-', lw=3.5, label=str(persistence_months)+str(inum_stocks_choices))
            elif persistence_months==16:
                plt.plot(plotdates, cumu_dynamic_system, 'y-', lw=3.5, label=str(persistence_months)+str(inum_stocks_choices))
            elif persistence_months==19:
                plt.plot(plotdates, cumu_dynamic_system, 'r-', lw=3.5, label=str(persistence_months)+str(inum_stocks_choices))
            else:
                plt.plot(plotdates, cumu_dynamic_system, label=str(persistence_months)+str(inum_stocks_choices))

            performance_text = str(datetime.date.today()) + "," + \
                               str(inum_sort_choice).replace(',',';') + "," + \
                               str(inum_stocks_choices).replace(',',';') + "," + \
                               str(persistence_months) + "," + \
                               str(cumu_dynamic_system[-1]) + "," + \
                               str(persistence_DD[-1]) + "," + \
                               str(persistence_mid_DD[-1]) + "," + \
                               str(persistence_recent_DD[-1]) + "," + \
                               str(persistence_sortinos[-1]) + "," + \
                               str(persistence_mid_sortinos[-1]) + "," + \
                               str(persistence_recent_sortinos[-1]) + "," + \
                               str(persistence_sharpes[-1]) + "," + \
                               str(persistence_mid_sharpes[-1]) + "," + \
                               str(persistence_recent_sharpes[-1]) + "\n"

            with open(csv_file, 'a') as f:
                f.write(performance_text)


# print list of final values with id
for id in range(len(persistence_recent_DD)):
    print(format(id,'03d'), '{:15,.0f}'.format(persistence_series_values[id][-1]))

plt.legend(fontsize=9)

plt.close(2)
plt.figure(2, figsize=(20,15))
plt.grid(True)
'''
plt.plot(persistence_values,final_values/np.max(final_values),label='final_value')
plt.plot(persistence_values,persistence_sortinos,label='sortino')
plt.plot(persistence_values,persistence_mid_sortinos,label='mid_sortino')
plt.plot(persistence_values,persistence_recent_sortinos,label='recent_sortino')
plt.plot(persistence_values,persistence_sharpes,'--',label='sharpe')
plt.plot(persistence_values,persistence_mid_sharpes,'--',label='mid_sharpe')
plt.plot(persistence_values,persistence_recent_sharpes,'--',label='recent_sharpe')
'''
plt.plot(range(len(unique_id_list)),final_values/np.max(final_values),label='final_value')
plt.plot(range(len(unique_id_list)),persistence_sortinos,label='sortino')
plt.plot(range(len(unique_id_list)),persistence_mid_sortinos,label='mid_sortino')
plt.plot(range(len(unique_id_list)),persistence_recent_sortinos,label='recent_sortino')
plt.plot(range(len(unique_id_list)),persistence_sharpes,'--',label='sharpe')
plt.plot(range(len(unique_id_list)),persistence_mid_sharpes,'--',label='mid_sharpe')
plt.plot(range(len(unique_id_list)),persistence_recent_sharpes,'--',label='recent_sharpe')
plt.legend(fontsize=19)



plt.close(3)
plt.figure(3,figsize=(20,15))
plt.rcParams['font.size'] = 24
plt.rcParams['legend.fontsize'] = 'large'
#plt.rcParams['text.Text'] = 'large'
plt.clf()
plt.grid(True)
plt.yscale('log')

id = np.argmax(final_values)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'final_value')
plot_text = (unique_id_list[id] + ' '*35)[:55] + \
            '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
            format(persistence_sharpes[id],'5.2f') + \
            format(persistence_mid_sharpes[id],'5.2f') + \
            format(persistence_recent_sharpes[id],'5.2f') + \
            ' final_value' + \
            format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
            format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
            "\n"
xid = np.argsort(final_values)
sum_id_ranks = (xid/10.).astype('int')
weighted_sum_id_ranks = (xid/10.).astype('int')*4

id = np.argmax(persistence_sortinos)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_sortinos')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_sortinos' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_sortinos)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')

id = np.argmax(persistence_mid_sortinos)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_mid_sortinos')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_mid_sortinos' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_mid_sortinos)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*2

id = np.argmax(persistence_recent_sortinos)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_recent_sortinos')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_recent_sortinos' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_recent_sortinos)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*3

id = np.argmax(persistence_sharpes)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_sharpes')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_sharpes' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_sharpes)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')

id = np.argmax(persistence_mid_sharpes)
plt.plot(plotdates[1:],persistence_series_values[id][1:],lw=2,label=str(id)+"__"+unique_id_list[id]+'persistence_mid_sharpes')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_mid_sharpes' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_mid_sharpes)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*2

id = np.argmax(persistence_recent_sharpes)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_recent_sharpes')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_recent_sharpes' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_recent_sharpes)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*3

id = np.argmax(persistence_DD)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_DD')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_DD' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_DD)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')

id = np.argmax(persistence_mid_DD)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_mid_DD')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_mid_DD' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_mid_DD)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*2

id = np.argmax(persistence_recent_DD)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'persistence_recent_DD')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' persistence_recent_DD' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
id = np.argsort(persistence_recent_DD)
sum_id_ranks += (id/10.).astype('int')
weighted_sum_id_ranks += (id/10.).astype('int')*3

id = np.argmax(sum_id_ranks)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'summed ranks')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' summed ranks' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"

id = np.argmax(weighted_sum_id_ranks)
plt.plot(plotdates[1:],persistence_series_values[id][1:],label=str(id)+"__"+unique_id_list[id]+'weighted sum ranks')
plot_text = plot_text + (unique_id_list[id] + ' '*35)[:55] + \
                        '{:15,.0f}'.format(persistence_series_values[id][-1]) + \
                        format(persistence_sharpes[id],'5.2f') + \
                        format(persistence_mid_sharpes[id],'5.2f') + \
                        format(persistence_recent_sharpes[id],'5.2f') + \
                        ' weighted sum ranks' + \
                        format(persistence_sharpes[id]+persistence_mid_sharpes[id]+persistence_recent_sharpes[id],'5.2f') + \
                        format(.2*persistence_sharpes[id]+.3*persistence_mid_sharpes[id]+.5*persistence_recent_sharpes[id],'5.2f') + \
                        "\n"
#plt.legend(fontsize=14)
plt.legend(fontsize=14)
plt.savefig(os.path.join(_performance_folder,'persistence_value_plot.png'), format='png')

'''
plt.clf()
plt.grid(True)
plt.yscale('log')

ids = [11,23,51,81,91,101,111,120,121,131]
for id in ids:
    mid_sortino = np.array(persistence_series_values[id])
    srtno = format(allstats(mid_sortino).sortino(),'4.2f')
    plt.plot(plotdates,persistence_series_values[id],label=unique_id_list[id]+str(id)+" "+srtno)

plt.legend()
plt.savefig(os.path.join(_performance_folder,_persistence_filename_prefix+'_plot2.png'), format='png')
'''
# print a summary table
print("\n\n\n" + plot_text)
