#Nama: Bernard Susanto
#NIM: 12220123
#UAS Prokom

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import streamlit as st

st.title("Ujian Akhir Semester Program Komputasi")
st.header("Bernard Susanto/12220123")

listnamanegara = list()
listkodenegara = list()

fhand = open('kode_negara_lengkap.json')
data = json.load(fhand)             #membaca file json
for negara in data:                 #loop pada tiap negara di file json
    listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
    datanamanegara = listoftp[0]    #data nama negara pada tuple pertama
    namanegara = datanamanegara[1]  #nama negara pada tuple indeks pertama
    listnamanegara.append(namanegara)
    datakodenegara = listoftp[2]    #data kode negara pada tuple ketiga
    kodenegara = datakodenegara[1]  #kode negara pada tuple indeks pertama
    listkodenegara.append(kodenegara)

kamus = dict(zip(listnamanegara,listkodenegara))        #memasangkan masing-masing nama dan kode negara pada dictionary

#Soal 1  
st.subheader("Grafik Produksi Minyak Mentah Negara pada Setiap Tahun")
masukanuser = st.text_input("Masukkan Nama Negara: ")

if masukanuser in listnamanegara:
    kodeinput = kamus[masukanuser]   #kode negara yang tepat diassign sesuai dengan nama negara masukan user
else:
    st.error("Nama negara tidak dapat ditemukan")    

df = pd.read_csv('produksi_minyak_mentah.csv')
df.produksi = df.produksi.astype(int)           #Menghilangkan titik pada data produksi
df_indexed = df.set_index("kode_negara")        #Mengubah index menjadi kode negara
datasoal1 = df_indexed.loc[kodeinput]            #Men-slice data hanya sesuai input negara dari user

fig, ax = plt.subplots()
ax.bar(datasoal1["tahun"], datasoal1["produksi"])
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
st.pyplot(fig)

#Soal 2
st.subheader("Grafik Produksi Terbesar Minyak Mentah Negara pada Tahun Tertentu")
Bnegara = st.number_input("Masukkan berapa besar negara: ",min_value=1,max_value=200)
tahuninput = st.number_input("Masukkan tahun (1971-2015): ",min_value=1971,max_value=2015)

df_indexed = df.set_index("tahun")              #Mengubah index menjadi tahun
dftahun = df_indexed.loc[int(tahuninput)]       #Men-slice data hanya sesuai input tahun dari user
produksi_sorted = dftahun.sort_values(["produksi"], ascending = False)  #mengurutkan data produksi dari terbesar ke terkecil
datasoal2 = produksi_sorted.head(int(Bnegara))  #mengambil data B-besar negara inputan user

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(datasoal2["kode_negara"])]
fig, ax = plt.subplots()
ax.bar(datasoal2["kode_negara"], datasoal2["produksi"],color=colors)
ax.set_xlabel("Kode Negara", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
st.pyplot(fig)

#Soal2b
st.subheader("Grafik Produksi Terkecil Minyak Mentah Negara pada Tahun Tertentu")
Bnegarakecil = st.number_input("Masukkan jumlah negara terendah: ",min_value=1,max_value=200)
tahuninputkecil = st.number_input("Masukkan tahun  (1971-2015): ",min_value=1971,max_value=2015)

dftahun2b = df_indexed[df_indexed["produksi"]!=0]    #Menghilangkan 0 pada data produksi
dftahun2b1 = dftahun2b.loc[int(tahuninputkecil)]
produksi_sorted1 = dftahun2b1.sort_values(["produksi"],ascending = True) #Mengatur agar urutan dari produksi terkecil
datasoal2b = produksi_sorted1.head(int(Bnegarakecil))
                                   
colors = cmap.colors[:len(datasoal2b["kode_negara"])]
fig, ax = plt.subplots()
ax.bar(datasoal2b["kode_negara"], datasoal2b["produksi"],color=colors)
ax.set_xlabel("Kode Negara", fontsize=12)
ax.set_ylabel("Produksi", fontsize=12)
st.pyplot(fig)

#Soal 3
st.subheader("Grafik Produksi Kumulatif Minyak Mentah B-Besar Negara")
Bnegarak = st.number_input("Masukkan jumlah besar negara: ",min_value=1,max_value=200)

listkodenegara1 = list(dftahun["kode_negara"])  #Mengambil deretan kode negara dari data di soal sebelumnya
                                                #Dikarenakan ketiadaan negara Afghanistan pada file csv yang diberikan
df_indexed = df.set_index("kode_negara")        #Mengubah index menjadi kode negara
listkodenegara2 = list()
listkproduksi = list()

for negara_i in listkodenegara1:                
    dftiapnegara = df_indexed.loc[negara_i]        #Data pada negara tertentu
    dataproduksi = list(dftiapnegara["produksi"])  #Memasukkan data produksi suatu negara ke dalam list untuk dijumlahkan
    kumulatifproduksi = sum(dataproduksi)           #Menjumlahkan data produksi untuk mendapat kumulatif produksi
    listkodenegara2.append(negara_i)                #Memasukkan ke dalam list
    listkproduksi.append(kumulatifproduksi)

dfsoal3 = {"Kode_Negara":listkodenegara2,"Kumulatif_Produksi":listkproduksi} 
datasoal3 = pd.DataFrame(dfsoal3)      #Membuat 2 list tadi ke dalam dataframe
datasoal3 = datasoal3.sort_values(["Kumulatif_Produksi"],ascending = False) #Mengatur agar urutan dari kumulatif terbesar
datasoal3top = datasoal3.head(int(Bnegarak))     #Menampilkan hanya data B-besar negara berdasarkan kumulatif

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(datasoal3top["Kode_Negara"])]
fig, ax = plt.subplots()
ax.bar(datasoal3top["Kode_Negara"],datasoal3top["Kumulatif_Produksi"],color=colors)
ax.set_xlabel("Kode Negara", fontsize=12)
ax.set_ylabel("Kumulatif Produksi (x10^7)", fontsize=12)
st.pyplot(fig)


#Soal 4
st.subheader("Informasi Tambahan")
tahuninput1 = st.number_input("Masukkan tahun-T (1971-2015): ",min_value=1971,max_value=2015)

df_indexed = df.set_index("tahun")              #Mengubah index menjadi tahun
dftahun = df_indexed.loc[int(tahuninput1)]       #Men-slice data hanya sesuai input tahun dari user

#Negara Produksi terbesar tahun-T
datacarikode = dftahun.sort_values(["produksi"],ascending = False) #Mengatur agar urutan dari produksi terbesar
datacarikode = datacarikode.head(1)                #negara dengan produksi terbesar di tahun tertentu
datacarikode = datacarikode["kode_negara"]
kodetercari = datacarikode.values[0]    #Mendapatkan kode negara dengan produksi terbesar

for negara in data:                 #loop pada tiap negara di file json
    listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
    kodeterbesar = listoftp[2] 
    if kodeterbesar[1] != kodetercari:          #Mencari tuple yang sesuai dengan kode tercari
        continue
    else:
        namaterbesar = listoftp[0]
        namaterbesar = namaterbesar[1]
        kodeterbesar = listoftp[2]
        kodeterbesar = kodeterbesar[1]
        regionterbesar = listoftp[5]
        regionterbesar = regionterbesar[1]
        subregionterbesar = listoftp[6]
        subregionterbesar = subregionterbesar[1]
        st.markdown("**Data Negara dengan Produksi Tahun-T Terbesar:**")
        st.write("Nama Negara: ",namaterbesar)
        st.write("Kode Negara: ",kodeterbesar)
        st.write("Region Negara: ",regionterbesar)
        st.write("Subregion Negara: ",subregionterbesar)
        
#Negara Produksi terbesar kumulatif
datasoal3b = datasoal3.head(1)               #Mencari negara dengan produksi kumulatif terbesar
datakterbesar = datasoal3b["Kode_Negara"]       #Menentukan kode negaranya
kodetercari1 = datakterbesar.values[0]

for negara in data:                 #loop pada tiap negara di file json
    listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
    kodeterbesar1 = listoftp[2] 
    if kodeterbesar1[1] != kodetercari1:          #Mencari tuple yang sesuai dengan kode tercari1
        continue
    else:
        namakterbesar = listoftp[0]
        namakterbesar = namakterbesar[1]
        kodekterbesar = listoftp[2]
        kodekterbesar = kodekterbesar[1]
        regionkterbesar = listoftp[5]
        regionkterbesar = regionkterbesar[1]
        subregionkterbesar = listoftp[6]
        subregionkterbesar = subregionkterbesar[1]
        st.markdown("**Data Negara dengan Produksi Kumulatif Terbesar:**")
        st.write("Nama Negara: ",namakterbesar)
        st.write("Kode Negara: ",kodekterbesar)
        st.write("Region Negara: ",regionkterbesar)
        st.write("Subregion Negara: ",subregionkterbesar)

#Negara Produksi terkecil tahun-T
dftahun1 = dftahun[dftahun["produksi"]!=0]    #Menghilangkan 0 pada data produksi
datacarikode2 = dftahun1.sort_values(["produksi"],ascending = True) #Mengatur agar urutan dari produksi terkecil
datacarikode2 = datacarikode2.head(1)                #negara dengan produksi terkecil di tahun tertentu
datacarikode2 = datacarikode2["kode_negara"]
kodetercari2 = datacarikode2.values[0]    #Mendapatkan kode negara dengan produksi terkecil

for negara in data:                 #loop pada tiap negara di file json
    listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
    kodeterkecil = listoftp[2] 
    if kodeterkecil[1] != kodetercari2:          #Mencari tuple yang sesuai dengan kode tercari2
        continue
    else:
        namaterkecil = listoftp[0]
        namaterkecil = namaterkecil[1]
        kodeterkecil = listoftp[2]
        kodeterkecil = kodeterkecil[1]
        regionterkecil = listoftp[5]
        regionterkecil = regionterkecil[1]
        subregionterkecil = listoftp[6]
        subregionterkecil = subregionterkecil[1]
        st.markdown("**Data Negara dengan Produksi Tahun-T Terkecil (Bukan 0):**")
        st.write("Nama Negara: ",namaterkecil)
        st.write("Kode Negara: ",kodeterkecil)
        st.write("Region Negara: ",regionterkecil)
        st.write("Subregion Negara: ",subregionterkecil)
        
#Negara Produksi terkecil kumulatif
datasoal3k = datasoal3[datasoal3["Kumulatif_Produksi"]!=0]    #Menghilangkan nilai 0 pada data kumulatif produksi
datasoal3k = datasoal3k.tail(1)               #Mencari negara dengan produksi kumulatif terkecil
datakterkecil = datasoal3k["Kode_Negara"]       #Menentukan kode negaranya
kodetercari3 = datakterkecil.values[0]      #Mendapat kode negara dengan kumulatif produksi terkecil

for negara in data:                 #loop pada tiap negara di file json
    listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
    kodeterkecil1 = listoftp[2] 
    if kodeterkecil1[1] != kodetercari3:          #Mencari tuple yang sesuai dengan kode tercari3
        continue
    else:
        namakterkecil = listoftp[0]
        namakterkecil = namakterkecil[1]
        kodekterkecil = listoftp[2]
        kodekterkecil = kodekterkecil[1]
        regionkterkecil = listoftp[5]
        regionkterkecil = regionkterkecil[1]
        subregionkterkecil = listoftp[6]
        subregionkterkecil = subregionkterkecil[1]
        st.markdown("**Data Negara dengan Produksi Kumulatif Terkecil (Bukan 0):**")
        st.write("Nama Negara: ",namakterkecil)
        st.write("Kode Negara: ",kodekterkecil)
        st.write("Region Negara: ",regionkterkecil)
        st.write("Subregion Negara: ",subregionkterkecil)

#Negara dengan Produksi 0 Tahun-T
df0produksi = dftahun.sort_values(["produksi"],ascending = True)
df0produksi_indexed = df0produksi.set_index("produksi")  
df0produksi1 = df0produksi_indexed.loc["0"]
listnegara0 = list(df0produksi1["kode_negara"])

st.markdown("**Data Negara dengan Produksi 0 Tahun-T:**")
listnama0 = []
listkode0 = []
listregion0 = []
listsubregion0 = []

for negara0 in listnegara0:         #loop pada negara0 di list negara dengan produksi 0 tahun T
    for negara in data:                 #loop pada tiap negara di file json
        listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
        kodenegara0produksi = listoftp[2] 
        if kodenegara0produksi[1] != negara0:          #Mencari tuple yang sesuai dengan negara0
            continue
        else:
            nama0 = listoftp[0]
            nama0 = nama0[1]
            listnama0.append(nama0)
            kode0 = listoftp[2]
            kode0 = kode0[1]
            listkode0.append(kode0)
            region0 = listoftp[5]
            region0 = region0[1]
            listregion0.append(region0)
            subregion0 = listoftp[6]
            subregion0 = subregion0[1]
            listsubregion0.append(subregion0)

dfsoal40 = {"Nama negara":listnama0,"Kode Negara":listkode0, "Region Negara":listregion0,"Subregion Negara":listsubregion0} #membuat 4 list ke bentuk dataframe
datasoal40 = pd.DataFrame(dfsoal40)
datasoal40jadi = datasoal40.set_index("Nama negara") 
st.dataframe(datasoal40jadi)

#Negara Produksi 0 Kumulatif
df0kproduksi_indexed = datasoal3.set_index("Kumulatif_Produksi")  
df0kproduksi1 = df0kproduksi_indexed.loc[0]
listnegarak0 = list(df0kproduksi1["Kode_Negara"])

st.markdown("**Data Negara dengan Produksi Kumulatif 0:**")
listnama0k = []
listkode0k = []
listregion0k = []
listsubregion0k = []

for negarak0 in listnegarak0:         #loop pada negara0 di list negara dengan produksi kumulatif 0
    for negara in data:                 #loop pada tiap negara di file json
        listoftp = [(kategori,hasil) for kategori,hasil in negara.items()] #mengubah dictionaries menjadi list of tuples
        kodenegara0kproduksi = listoftp[2] 
        if kodenegara0kproduksi[1] != negarak0:          #Mencari tuple yang sesuai dengan negarak0
            continue
        else:
            nama0k = listoftp[0]
            nama0k = nama0k[1]
            listnama0k.append(nama0k)
            kode0k = listoftp[2]
            kode0k = kode0k[1]
            listkode0k.append(kode0k)
            region0k = listoftp[5]
            region0k = region0k[1]
            listregion0k.append(region0k)
            subregion0k = listoftp[6]
            subregion0k = subregion0k[1]
            listsubregion0k.append(subregion0k)
            
dfsoal40k = {"Nama Negara":listnama0k,"Kode Negara":listkode0k, "Region Negara":listregion0k,"Subregion Negara":listsubregion0k} 
datasoal40k = pd.DataFrame(dfsoal40k)
datasoal40kjadi = datasoal40k.set_index("Nama Negara")
st.dataframe(datasoal40kjadi)
