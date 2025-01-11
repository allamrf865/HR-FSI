import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import pandas as pd

# Data awal: Masalah dan penyebab (5 Why)
default_masalah = {
    "Masalah": [
        "Penurunan Motivasi Anggota",
        "Branding Kurang Optimal",
        "Manajerial Kurang Baik",
        "Sistem Reward Anggota",
        "Waktu Publikasi Kurang Teratur",
        "Alur Administrasi Kurang Jelas",
        "Tidak Ada Panduan yang Jelas untuk Setiap Proker",
        "Kurangnya Follow-Up",
        "Penurunan Akademik Akibat Kerja Organisasi",
        "Belum Ada Work Life Balance"
    ],
    "Penyebab": [
        ["Kurangnya feedback positif", "Kurangnya apresiasi", "Tidak ada evaluasi", "Minimnya komunikasi", "Tidak ada pelatihan"],
        ["Minimnya alokasi dana promosi", "Tidak ada strategi branding", "Kurang tim media", "Desain kurang menarik", "Tidak ada media sosial aktif"],
        ["Pemimpin tidak memberikan arahan jelas", "Kepemimpinan tidak konsisten", "Delegasi buruk", "Kurangnya pengawasan", "Tidak ada pelatihan manajerial"],
        ["Tidak ada penghargaan yang menarik", "Tidak ada insentif", "Reward tidak relevan", "Tidak ada target pencapaian", "Kurang apresiasi publik"],
        ["Tidak ada jadwal tetap", "Penundaan yang sering", "Kurang koordinasi", "Tidak ada deadline jelas", "Kurangnya tanggung jawab"],
        ["Tidak ada SOP baku", "Proses berbelit", "Kurangnya template dokumen", "Tidak ada pembagian tugas", "Tidak ada sistem otomatisasi"],
        ["Proker tidak memiliki guideline", "Tim tidak paham alur kerja", "Tidak ada template jelas", "Kurangnya evaluasi", "Tidak ada supervisi"],
        ["Tidak ada mekanisme evaluasi", "Tidak ada follow-up plan", "Kurang tindak lanjut", "Tim tidak punya tanggung jawab", "Tidak ada feedback yang jelas"],
        ["Anggota terlalu fokus pada organisasi", "Tidak ada pembagian waktu", "Kurang koordinasi akademik", "Tidak ada bantuan tim", "Deadline berbenturan"],
        ["Beban kerja terlalu tinggi", "Tidak ada work life balance", "Tim kekurangan anggota", "Tidak ada delegasi tugas", "Kurangnya waktu istirahat"]
    ],
    "Koneksi Masalah": [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
        (5, 6), (6, 7), (7, 8), (8, 9), (0, 9)
    ]
}

# Data KPI/TOPSIS untuk tingkat kinerja anggota
kinerja_anggota = {
    "Anggota": ["Anggota A", "Anggota B", "Anggota C", "Anggota D", "Anggota E"],
    "KPI": [85, 75, 90, 70, 60],
    "TOPSIS": [0.85, 0.65, 0.92, 0.58, 0.48],
    "Workload": [70, 80, 50, 90, 60]
}

# Data beban kerja proker
beban_kerja_proker = {
    "Proker": ["Sirkumsisi", "Mabroh", "Pengobatan Massal", "Donor Darah", "Penggalangan Dana"],
    "Anggota A": [30, 10, 20, 25, 15],
    "Anggota B": [20, 15, 30, 20, 20],
    "Anggota C": [10, 20, 25, 30, 15],
    "Anggota D": [15, 25, 15, 20, 25],
    "Anggota E": [25, 30, 10, 15, 25]
}

# Fungsi untuk menambahkan masalah baru
def tambah_masalah():
    st.subheader("Masukkan Masalah Baru dan 5 Why Penyebabnya")
    masalah_baru = st.text_input("Masalah baru:")
    penyebab_baru = []
    for i in range(5):
        penyebab = st.text_input(f"Penyebab {i+1}:", key=f"penyebab_{i}")
        if penyebab:
            penyebab_baru.append(penyebab)

    if st.button("Tambahkan Masalah Baru"):
        if masalah_baru and len(penyebab_baru) == 5:
            default_masalah["Masalah"].append(masalah_baru)
            default_masalah["Penyebab"].append(penyebab_baru)
            st.success("Masalah baru dan penyebab berhasil ditambahkan!")
        else:
            st.error("Pastikan semua input terisi!")

# Fungsi visualisasi 1: Masalah vs Penyebab (3D Network)
def visualisasi_masalah_vs_penyebab(data):
    G = nx.Graph()
    for idx, (m, penyebab_list) in enumerate(zip(data["Masalah"], data["Penyebab"])):
        G.add_node(f"Masalah {idx+1}: {m}", group="Masalah")
        for penyebab in penyebab_list:
            G.add_node(f"Penyebab {idx+1}: {penyebab}", group="Penyebab")
            G.add_edge(f"Masalah {idx+1}: {m}", f"Penyebab {idx+1}: {penyebab}")

    pos = nx.spring_layout(G, dim=3, seed=42)
    node_x, node_y, node_z, node_text, node_color = [], [], [], [], []
    edge_x, edge_y, edge_z = [], [], []

    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(node)
        if "Masalah" in node:
            node_color.append("rgb(244,109,67)")
        else:
            node_color.append("rgb(67,244,109)")

    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='rgba(125,125,125,0.8)', width=2),
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(size=10, color=node_color, opacity=0.8),
        text=node_text,
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Pemetaan Masalah vs Penyebab (3D Network)",
        scene=dict(
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
            zaxis_title="Z Axis"
        ),
        template="plotly_dark"
    )
    return fig

# Fungsi visualisasi 2: Hubungan Antar Masalah (3D Network)
def visualisasi_hubungan_antar_masalah(data):
    G = nx.Graph()

    for idx, m in enumerate(data["Masalah"]):
        G.add_node(f"Masalah {idx+1}: {m}")
    for edge in data["Koneksi Masalah"]:
        G.add_edge(f"Masalah {edge[0]+1}: {data['Masalah'][edge[0]]}",
                   f"Masalah {edge[1]+1}: {data['Masalah'][edge[1]]}")

    pos = nx.spring_layout(G, dim=3, seed=42)

    node_x, node_y, node_z, node_text, node_color = [], [], [], [], []
    edge_x, edge_y, edge_z = [], [], []

    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(node)
        node_color.append("rgb(244,109,67)")

    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='rgba(200,200,200,0.8)', width=2),
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(size=12, color=node_color, opacity=0.9),
        text=node_text,
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Hubungan Antar Masalah (3D Network)",
        scene=dict(
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
            zaxis_title="Z Axis"
        ),
        template="plotly_dark"
    )
    return fig

# Fungsi visualisasi 3: Heatmap 3D
def visualisasi_heatmap_3d(data):
    num_masalah = len(data["Masalah"])
    matrix = np.random.rand(num_masalah, num_masalah)

    fig = go.Figure(data=go.Surface(z=matrix))
    fig.update_layout(
        title="Heatmap 3D Korelasi Antar Masalah",
        scene=dict(
            xaxis_title="Masalah",
            yaxis_title="Masalah",
            zaxis_title="Intensitas Korelasi"
        ),
        template="plotly_dark"
    )
    return fig

# Fungsi visualisasi 4: Tingkat Kinerja Anggota (3D Bar Chart Horizontal)
def visualisasi_kinerja_bar(data):
    fig = go.Figure()

    for i, anggota in enumerate(data["Anggota"]):
        fig.add_trace(go.Bar(
            x=[data["KPI"][i]],
            y=[anggota],
            orientation='h',
            name=f"KPI {anggota}",
            marker=dict(color=f'rgba({50+i*40}, {150+i*30}, {255-i*30}, 0.8)')
        ))
        fig.add_trace(go.Bar(
            x=[data["TOPSIS"][i]*100],
            y=[anggota],
            orientation='h',
            name=f"TOPSIS {anggota}",
            marker=dict(color=f'rgba({255-i*30}, {50+i*30}, {150+i*40}, 0.8)')
        ))

    fig.update_layout(
        title="Visualisasi Kinerja Anggota (3D Bar Chart Horizontal)",
        xaxis_title="Persentase",
        yaxis_title="Anggota",
        barmode='group',
        template="plotly_dark"
    )
    return fig

# Fungsi visualisasi 5: Pembagian Beban Kerja Proker (3D Stacked Bar Chart)
def visualisasi_beban_kerja_3d(data):
    df = pd.DataFrame(data)
    fig = go.Figure()

    for col in df.columns[1:]:
        fig.add_trace(go.Bar(
            x=df["Proker"],
            y=df[col],
            name=col,
            text=col
        ))

    fig.update_layout(
        title="Pembagian Beban Kerja (3D Stacked Bar Chart)",
        xaxis_title="Proker",
        yaxis_title="Beban Kerja",
        barmode='stack',
        template="plotly_dark"
    )
    return fig

# Fungsi utama untuk menampilkan semua visualisasi
def visualisasi_semua():
    st.subheader("Visualisasi 3D")
    st.write("1. Masalah vs Penyebab")
    st.plotly_chart(visualisasi_masalah_vs_penyebab(default_masalah), use_container_width=True)

    st.write("2. Hubungan Antar Masalah")
    st.plotly_chart(visualisasi_hubungan_antar_masalah(default_masalah), use_container_width=True)

    st.write("3. Heatmap 3D Korelasi Antar Masalah")
    st.plotly_chart(visualisasi_heatmap_3d(default_masalah), use_container_width=True)

    st.write("4. Tingkat Kinerja Anggota")
    st.plotly_chart(visualisasi_kinerja_bar(kinerja_anggota), use_container_width=True)

    st.write("5. Pembagian Beban Kerja")
    st.plotly_chart(visualisasi_beban_kerja_3d(beban_kerja_proker), use_container_width=True)

# Fungsi utama
def main():
    st.title("Visualisasi Masalah dan Kinerja (3D)")
    st.sidebar.title("Navigasi")
    pilihan = st.sidebar.selectbox("Pilih Halaman", ["Tambah Masalah Baru", "Visualisasi 3D"])

    if pilihan == "Tambah Masalah Baru":
        tambah_masalah()
    elif pilihan == "Visualisasi 3D":
        visualisasi_semua()

if __name__ == "__main__":
    main()
