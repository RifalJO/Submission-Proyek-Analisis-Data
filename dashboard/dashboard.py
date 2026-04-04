# -*- coding: utf-8 -*-
"""
Dashboard Analisis Kualitas Udara Beijing
Penulis: Muhamad Rizki Rifaldi
Proyek Submission Dicoding - Analisis Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import st_folium
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Kualitas Udara Beijing",
    page_icon="🌫️",
    layout="wide"
)

# Load data dengan caching
@st.cache_data
def load_data():
    # Gunakan path absolut berdasarkan lokasi file dashboard
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, 'main_data.csv')
    df = pd.read_csv(data_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

# Koordinat stasiun
STATION_COORDS = {
    'Aotizhongxin': {'lat': 39.9829, 'lon': 116.3971},
    'Changping': {'lat': 40.2175, 'lon': 116.2309},
    'Dingling': {'lat': 40.2925, 'lon': 116.2200},
    'Dongsi': {'lat': 39.9290, 'lon': 116.4175},
    'Guanyuan': {'lat': 39.9290, 'lon': 116.3390},
    'Gucheng': {'lat': 39.9140, 'lon': 116.1840},
    'Huairou': {'lat': 40.3281, 'lon': 116.6283},
    'Nongzhanguan': {'lat': 39.9368, 'lon': 116.4605},
    'Shunyi': {'lat': 40.1270, 'lon': 116.6557},
    'Tiantan': {'lat': 39.8863, 'lon': 116.4079},
    'Wanliu': {'lat': 39.9870, 'lon': 116.2882},
    'Wanshouxigong': {'lat': 39.8780, 'lon': 116.3520}
}

# Warna kategori AQI (darker untuk kontras lebih baik)
AQI_COLORS = {
    'Baik': '#27ae60',
    'Sedang': '#d4ac0d',
    'Tidak Sehat': '#d35400',
    'Sangat Tidak Sehat': '#c0392b',
    'Berbahaya': '#7d3c98'
}

def get_aqi_category(pm25):
    """Klasifikasikan kategori AQI berdasarkan PM2.5"""
    if pm25 <= 12:
        return 'Baik'
    elif pm25 <= 35.4:
        return 'Sedang'
    elif pm25 <= 55.4:
        return 'Tidak Sehat'
    elif pm25 <= 150.4:
        return 'Sangat Tidak Sehat'
    else:
        return 'Berbahaya'

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("---")

# Filter stasiun
all_stations = sorted(df['station'].unique())
selected_stations = st.sidebar.multiselect(
    "Pilih Stasiun:",
    options=all_stations,
    default=all_stations,
    help="Pilih satu atau lebih stasiun untuk dianalisis"
)

# Filter tahun
years = sorted(df['datetime'].dt.year.unique())
selected_year = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=years,
    index=len(years)-1,
    help="Pilih tahun untuk melihat data pada tahun tersebut"
)

# Filter musim
seasons = ['Semua', 'Semi', 'Panas', 'Gugur', 'Dingin']
selected_season = st.sidebar.selectbox(
    "Pilih Musim:",
    options=seasons,
    index=0,
    help="Filter data berdasarkan musim"
)

st.sidebar.markdown("---")
st.sidebar.info(f"**Total data:** {len(df):,} pengukuran")

# Filter data berdasarkan pilihan user
filtered_df = df.copy()

if selected_stations:
    filtered_df = filtered_df[filtered_df['station'].isin(selected_stations)]

filtered_df = filtered_df[filtered_df['datetime'].dt.year == selected_year]

if selected_season != 'Semua':
    filtered_df = filtered_df[filtered_df['musim'] == selected_season]

# Hitung statistik per stasiun
station_stats = df.groupby('station').agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'NO2': 'mean',
    'SO2': 'mean',
    'CO': 'mean',
    'O3': 'mean'
}).round(2)

station_stats.columns = ['avg_pm25', 'avg_pm10', 'avg_no2', 'avg_so2', 'avg_co', 'avg_o3']
station_stats['aqi_category'] = station_stats['avg_pm25'].apply(get_aqi_category)
station_stats = station_stats.reset_index()
station_stats = station_stats.sort_values('avg_pm25', ascending=False)

# Judul Dashboard
st.title("🌫️ Dashboard Analisis Kualitas Udara Beijing")
st.markdown("**Penulis:** Muhamad Rizki Rifaldi | **Submission Dicoding**")
st.markdown("---")

# Buat tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Ringkasan Umum",
    "📈 Tren & Pola Polusi",
    "🗺️ Peta Sebaran Polusi",
    "💡 Kesimpulan & Rekomendasi"
])

# ==================== TAB 1: RINGKASAN UMUM ====================
with tab1:
    st.header("📊 Ringkasan Umum Kualitas Udara")
    
    # Hitung metrik utama dari data yang difilter
    overall_pm25 = filtered_df['PM2.5'].mean()
    
    # Stasiun paling tercemar dan paling bersih dari data yang difilter
    if len(selected_stations) > 0:
        station_avg = filtered_df.groupby('station')['PM2.5'].mean()
        most_polluted = station_avg.idxmax()
        most_polluted_val = station_avg.max()
        cleanest = station_avg.idxmin()
        cleanest_val = station_avg.min()
    else:
        most_polluted = "N/A"
        most_polluted_val = 0
        cleanest = "N/A"
        cleanest_val = 0
    
    # 3 Kartu Metrik
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Rata-rata PM2.5",
            value=f"{overall_pm25:.2f} μg/m³",
            delta="Konsentrasi Partikel Halus",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Stasiun Paling Tercemar",
            value=most_polluted,
            delta=f"{most_polluted_val:.2f} μg/m³" if most_polluted != "N/A" else "N/A",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Stasiun Paling Bersih",
            value=cleanest,
            delta=f"{cleanest_val:.2f} μg/m³" if cleanest != "N/A" else "N/A",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Tabel Ringkasan
    st.subheader("📋 Tabel Ringkasan per Stasiun")
    
    # Tampilkan hanya stasiun yang dipilih
    display_stats = station_stats[station_stats['station'].isin(selected_stations)].copy()
    
    # Format untuk tampilan
    display_stats['avg_pm25'] = display_stats['avg_pm25'].round(2)
    display_stats['avg_pm10'] = display_stats['avg_pm10'].round(2)
    
    # Rename kolom
    display_stats = display_stats.rename(columns={
        'avg_pm25': 'Rata-rata PM2.5',
        'avg_pm10': 'Rata-rata PM10',
        'aqi_category': 'Kategori AQI'
    })
    
    # Fungsi untuk highlight warna berdasarkan kategori
    def highlight_category(val):
        if val in AQI_COLORS:
            return f'background-color: {AQI_COLORS[val]}; color: white; font-weight: bold'
        return ''
    
    # Tampilkan tabel dengan styling
    styled_table = display_stats[['station', 'Rata-rata PM2.5', 'Rata-rata PM10', 'Kategori AQI']].style
    styled_table = styled_table.map(highlight_category, subset=['Kategori AQI'])
    styled_table = styled_table.format({'Rata-rata PM2.5': '{:.2f}', 'Rata-rata PM10': '{:.2f}'})
    
    st.dataframe(styled_table, use_container_width=True, hide_index=True)
    
    st.caption("💡 **Cara membaca:** Tabel di atas menampilkan rata-rata konsentrasi PM2.5 dan PM10 untuk setiap stasiun, diurutkan dari yang paling tinggi. Warna pada kolom Kategori AQI menunjukkan tingkat bahaya polusi.")

# ==================== TAB 2: TREN & POLA POLUSI ====================
with tab2:
    st.header("📈 Tren & Pola Polusi PM2.5")
    
    # Chart 1: Tren Bulanan
    st.subheader("📅 Tren Rata-rata PM2.5 Bulanan")
    
    monthly_data = filtered_df.copy()
    monthly_data['year_month'] = monthly_data['datetime'].dt.to_period('M')
    monthly_avg = monthly_data.groupby(['year_month', 'station'])['PM2.5'].mean().reset_index()
    monthly_avg['year_month'] = monthly_avg['year_month'].astype(str)
    
    if len(selected_stations) > 0 and len(monthly_avg) > 0:
        fig1, ax1 = plt.subplots(figsize=(14, 6))
        
        for station in selected_stations:
            station_data = monthly_avg[monthly_avg['station'] == station]
            ax1.plot(station_data['year_month'], station_data['PM2.5'], 
                    marker='o', markersize=3, linewidth=1.5, label=station)
        
        ax1.set_xlabel('Bulan', fontsize=12)
        ax1.set_ylabel('Rata-rata PM2.5 (μg/m³)', fontsize=12)
        ax1.set_title('Tren Rata-rata PM2.5 Bulanan per Stasiun', fontsize=14, fontweight='bold')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax1.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig1)
    else:
        st.warning("Tidak ada data untuk ditampilkan dengan filter saat ini.")
    
    st.markdown("---")
    
    # Chart 2 & 3: Pola per Musim dan Waktu Hari
    col2_1, col2_2 = st.columns(2)
    
    with col2_1:
        st.subheader("🌤️ Rata-rata PM2.5 per Musim")
        
        if len(selected_stations) > 0:
            season_data = filtered_df[filtered_df['station'].isin(selected_stations)]
            season_avg = season_data.groupby('musim')['PM2.5'].mean()
            season_order = ['Semi', 'Panas', 'Gugur', 'Dingin']
            season_avg = season_avg.reindex(season_order)
            
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            colors_season = ['#95a5a6' if x < overall_pm25 else '#e74c3c' for x in season_avg.values]
            bars = ax2.bar(season_order, season_avg.values, color=colors_season, edgecolor='black')
            
            ax2.set_xlabel('Musim', fontsize=12)
            ax2.set_ylabel('Rata-rata PM2.5 (μg/m³)', fontsize=12)
            ax2.set_title('Pola PM2.5 Berdasarkan Musim', fontsize=14, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3)
            
            # Tambahkan label nilai
            for bar, val in zip(bars, season_avg.values):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                        f'{val:.1f}', ha='center', va='bottom', fontsize=10)
            
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.warning("Tidak ada data untuk ditampilkan.")
    
    with col2_2:
        st.subheader("🕐 Rata-rata PM2.5 per Waktu Hari")
        
        if len(selected_stations) > 0:
            time_data = filtered_df[filtered_df['station'].isin(selected_stations)]
            time_avg = time_data.groupby('waktu_hari')['PM2.5'].mean()
            time_order = ['Pagi', 'Siang', 'Sore', 'Malam']
            time_avg = time_avg.reindex(time_order)
            
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            colors_time = ['#3498db' if x < overall_pm25 else '#e74c3c' for x in time_avg.values]
            bars = ax3.bar(time_order, time_avg.values, color=colors_time, edgecolor='black')
            
            ax3.set_xlabel('Waktu dalam Sehari', fontsize=12)
            ax3.set_ylabel('Rata-rata PM2.5 (μg/m³)', fontsize=12)
            ax3.set_title('Pola PM2.5 Berdasarkan Waktu Hari', fontsize=14, fontweight='bold')
            ax3.grid(axis='y', alpha=0.3)
            
            # Tambahkan label nilai
            for bar, val in zip(bars, time_avg.values):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                        f'{val:.1f}', ha='center', va='bottom', fontsize=10)
            
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            st.warning("Tidak ada data untuk ditampilkan.")
    
    st.markdown("---")
    st.caption("💡 **Insight:** Polusi PM2.5 cenderung lebih tinggi pada musim dingin dan malam hari, sedangkan kualitas udara terbaik terjadi pada musim panas dan siang hari.")

# ==================== TAB 3: PETA SEBARAN POLUSI ====================
with tab3:
    st.header("🗺️ Peta Sebaran Polusi Beijing")
    
    # Buat peta interaktif
    m = folium.Map(location=[39.9042, 116.4074], zoom_start=10, tiles='CartoDB positron')
    
    # Tambahkan marker untuk setiap stasiun yang dipilih
    for station in selected_stations:
        station_data = station_stats[station_stats['station'] == station].iloc[0]
        lat = STATION_COORDS[station]['lat']
        lon = STATION_COORDS[station]['lon']
        color = AQI_COLORS[station_data['aqi_category']]
        
        # Popup content
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <h4 style="margin-bottom: 10px; color: {color};">{station}</h4>
            <b>Rata-rata PM2.5:</b> {station_data['avg_pm25']:.2f} μg/m³<br>
            <b>Rata-rata PM10:</b> {station_data['avg_pm10']:.2f} μg/m³<br>
            <b>Rata-rata NO2:</b> {station_data['avg_no2']:.2f} μg/m³<br>
            <b>Kategori AQI:</b> <span style="color: {color}; font-weight: bold;">{station_data['aqi_category']}</span>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=station_data['avg_pm25'] / 5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{station}: {station_data['avg_pm25']:.2f} μg/m³"
        ).add_to(m)
    
    # Legend with readable colors
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px;
                 background-color: rgba(255,255,255,0.95); border: 2px solid #333; z-index: 9999; font-size: 13px;
                 padding: 12px; border-radius: 8px; box-shadow: 3px 3px 8px rgba(0,0,0,0.4);">
        <h4 style="margin-top: 0; margin-bottom: 12px; font-weight: bold; color: #222;">Kategori AQI (PM2.5)</h4>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 22px; height: 22px; background-color: #27ae60; margin-right: 12px; border-radius: 50%; border: 2px solid #1a7a40;"></div>
            <span style="color: #1a7a40; font-weight: 600;">Baik (0–12)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 22px; height: 22px; background-color: #d4ac0d; margin-right: 12px; border-radius: 50%; border: 2px solid #9c7d0a;"></div>
            <span style="color: #7d6508; font-weight: 600;">Sedang (12–35.4)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 22px; height: 22px; background-color: #d35400; margin-right: 12px; border-radius: 50%; border: 2px solid #a04000;"></div>
            <span style="color: #a04000; font-weight: 600;">Tidak Sehat (35.4–55.4)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 22px; height: 22px; background-color: #c0392b; margin-right: 12px; border-radius: 50%; border: 2px solid #922b21;"></div>
            <span style="color: #922b21; font-weight: 600;">Sangat Tidak Sehat (55.4–150.4)</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 22px; height: 22px; background-color: #7d3c98; margin-right: 12px; border-radius: 50%; border: 2px solid #5b2c6f;"></div>
            <span style="color: #5b2c6f; font-weight: 600;">Berbahaya (>150.4)</span>
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Tampilkan peta
    st_folium(m, width=1200, height=600)
    
    st.markdown("---")
    
    # Tabel koordinat dan statistik
    st.subheader("📍 Data Koordinat dan Statistik Stasiun")
    
    coords_df = station_stats[station_stats['station'].isin(selected_stations)].copy()
    coords_df['latitude'] = coords_df['station'].apply(lambda x: STATION_COORDS[x]['lat'])
    coords_df['longitude'] = coords_df['station'].apply(lambda x: STATION_COORDS[x]['lon'])
    
    coords_display = coords_df[['station', 'latitude', 'longitude', 'avg_pm25', 'aqi_category']].copy()
    coords_display = coords_display.rename(columns={
        'avg_pm25': 'Rata-rata PM2.5',
        'aqi_category': 'Kategori AQI'
    })
    
    st.dataframe(coords_display, use_container_width=True, hide_index=True)
    
    st.caption("💡 **Cara membaca peta:** Ukuran lingkaran menunjukkan tingkat polusi (semakin besar = semakin polusi). Warna menunjukkan kategori AQI: hijau (Baik), kuning (Sedang), oranye (Tidak Sehat), merah (Sangat Tidak Sehat), ungu (Berbahaya).")

# ==================== TAB 4: KESIMPULAN & REKOMENDASI ====================
with tab4:
    st.header("💡 Kesimpulan & Rekomendasi")
    
    st.markdown("""
    ### 📌 Insight Utama
    
    Berdasarkan analisis data kualitas udara Beijing dari Maret 2013 hingga Februari 2017, berikut adalah temuan utama:
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        **🏭 Stasiun Paling Tercemar:**
        - **Changping** dan **Dingling** menunjukkan tingkat polusi PM2.5 tertinggi
        - Terletak di wilayah utara-barat Beijing
        - Dipengaruhi oleh kawasan industri dan aktivitas suburban
        
        **🌳 Stasiun Paling Bersih:**
        - **Huairou** dan **Shunyi** memiliki kualitas udara terbaik
        - Terletak di wilayah timur-laut dengan lebih banyak ruang terbuka hijau
        """)
    
    with col_b:
        st.markdown("""
        **📅 Pola Musiman:**
        - **Musim Dingin**: Polusi tertinggi (pemanas ruangan berbahan bakar batu bara)
        - **Musim Panas**: Kualitas udara terbaik (dispersi polutan lebih baik)
        
        **🕐 Pola Harian:**
        - **Malam (00-05)**: PM2.5 tertinggi (atmosfer stabil, polutan terperangkap)
        - **Siang (12-17)**: Kualitas udara terbaik (pencampuran atmosfer baik)
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### ❓ Jawaban Pertanyaan Bisnis
    
    **Pertanyaan 1:** *"Stasiun mana yang memiliki rata-rata polusi PM2.5 paling tinggi, dan bagaimana perbandingan tingkat polusi di seluruh 12 stasiun?"*
    
    **Jawaban:** Stasiun **Changping** memiliki rata-rata PM2.5 tertinggi, diikuti oleh **Dingling** dan **Wanliu**. Ketiga stasiun ini terletak di wilayah utara-barat Beijing. Stasiun dengan kualitas udara terbaik adalah **Huairou**, **Shunyi**, dan **Tiantan** yang berada di wilayah dengan lebih banyak ruang terbuka hijau dan jauh dari kawasan industri utama.
    
    ---
    
    **Pertanyaan 2:** *"Bagaimana pola polusi PM2.5 berubah sepanjang musim (Semi, Panas, Gugur, Dingin) dan waktu dalam sehari (Pagi, Siang, Sore, Malam)?"*
    
    **Jawaban:** 
    - **Berdasarkan Musim:** Polusi PM2.5 tertinggi terjadi pada **musim dingin** akibat peningkatan penggunaan pemanas berbahan bakar batu bara. Kualitas udara terbaik adalah pada **musim panas** karena kondisi atmosfer yang mendukung dispersi polutan dan curah hujan yang lebih tinggi.
    - **Berdasarkan Waktu Hari:** Konsentrasi PM2.5 tertinggi terjadi pada **malam hari (00-05)** ketika atmosfer stabil dan polutan terperangkap. Kualitas udara terbaik adalah pada **siang hari (12-17)** karena pencampuran atmosfer yang lebih baik.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Rekomendasi Kebijakan
    
    1. **Prioritas Pengawasan di Wilayah Utara-Barat:** Pemerintah Beijing perlu memprioritaskan monitoring dan penegakan standar emisi di kawasan Changping dan Dingling melalui inspeksi rutin terhadap kawasan industri.
    
    2. **Kampanye Kesadaran Publik Berdasarkan Waktu:** 
       - Musim dingin: Anjuran menggunakan masker dan membatasi aktivitas outdoor
       - Malam hingga pagi hari: Hindari olahraga outdoor pada jam-jam ini
    
    3. **Investasi Transportasi Hijau:** Memperluas jaringan kereta bawah tanah dan bus listrik, terutama di koridor yang menghubungkan wilayah utara-barat dengan pusat kota.
    
    4. **Sistem Peringatan Dini Terintegrasi:** Mengembangkan aplikasi mobile yang memberikan notifikasi real-time tentang kualitas udara dan rekomendasi kesehatan berdasarkan lokasi pengguna.
    
    5. **Penghijauan Strategis:** Menanam pohon dan mengembangkan koridor hijau di wilayah dengan polusi tinggi untuk membantu menyerap polutan.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📊 Sumber Data
    
    - **Dataset:** Air Quality Dataset dari Beijing, China
    - **Periode:** Maret 2013 - Februari 2017
    - **Frekuensi:** Pengukuran per jam
    - **Jumlah Stasiun:** 12 stasiun pengukuran
    - **Polutan yang Diukur:** PM2.5, PM10, SO2, NO2, CO, O3
    - **Data Meteorologi:** Temperatur, tekanan, kelembaban, curah hujan, kecepatan angin
    
    ---
    
    **Penulis:** Muhamad Rizki Rifaldi  
    **Proyek:** Submission Kelas Dicoding - Analisis Data
    """)

# Footer
st.markdown("---")
st.caption("Dashboard ini dibuat menggunakan Streamlit | Data sumber: Air Quality Dataset Beijing 2013-2017")
