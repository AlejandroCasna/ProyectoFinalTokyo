import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import psycopg2
import plotly.express as px
from src.help_graficos import Graficos
import streamlit_authenticator as stauth
import toml
import os





st.set_page_config(
    page_title="VoleyStats Pro",
    page_icon=":volleyball:",  
    layout="wide",  
    initial_sidebar_state="collapsed"  
)
secrets = toml.load("secrets.toml")
usuario = secrets["usuario"]
contrasenia = secrets["contrasenia"]


# Pide al usuario que ingrese la contraseña
password_placeholder = st.empty()
user_input = password_placeholder.text_input("Ingresa la contraseña:", type="password")

# Verifica si la contraseña ingresada es correcta
if user_input == contrasenia:
    # Elimina la celda de la contraseña si la contraseña es correcta
    password_placeholder.empty()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    class VoleyStatsApp:
        if 'programacion_activa' not in st.session_state:
            st.session_state['programacion_activa'] = False 
        def __init__(self):
            self.df = pd.DataFrame()
            st.set_option('deprecation.showPyplotGlobalUse', False)

        def _set_background(self, image_url):
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background: url("{image_url}");
                    background-size: cover;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        def _set_header_style(self, color, shadow_color):
            header_style = f"""
                <style>
                .stApp {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                }}
                .header-styles {{
                    font-size: 40px;
                    font-weight: bold;
                    color: {color};
                    text-align: center;
                    padding: 10px;
                    background-color: #F0F2F6;
                    border-radius: 10px;
                    margin: 25px;
                    box-shadow: 0 4px 8px 0 {shadow_color};
                }}
                </style>
            """
            st.markdown(header_style, unsafe_allow_html=True)

        def _show_image_and_info(self, team_name, image_url):
            st.sidebar.markdown(
                f'<img src="{image_url}" alt="Imagen de {team_name}" style="border-radius:20%; width:50%;">',
                unsafe_allow_html=True
            )
            df_equipo = pd.read_csv('../proyectofinaltokyo/data/Equipos_final.csv')
            # Mostrar información específica de la columna 'informacion' con saltos de línea
            informacion_equipo = df_equipo[df_equipo['Equipo'] == team_name]['informacion'].iloc[0]

            st.sidebar.markdown(f"\n{informacion_equipo}", unsafe_allow_html=True)

        def ejecutar_consulta(self, query):
            database_url = os.environ.get('DATABASE_URL_2')

            try:
                if not database_url:
                    with open('../proyectofinaltokyo/pass.txt', 'r') as file:   # pass.txt en .gitignore
                        database = file.read()
                        engine = create_engine(f"postgresql+psycopg2://{database}")
                else:
                    engine = create_engine(f"postgresql+psycopg2://{database_url}")

                with engine.connect() as connection:
                    df = pd.read_sql(query, connection)

                return df

            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")
                raise


        def pagina_inicio(self):
            

            self._set_background("https://integralspor.com/uploads/blog/detail/1618e792d4b1254221.jpg")
            self._set_header_style("#FF4B4B", "rgba(0,0,0,0.2)")

            st.markdown('<div class="header-styles">Bienvenidos a VoleyStats Pro</div>', unsafe_allow_html=True)

            presentacion = """<div style='color: #FFFFFF;font-size: 50px;'>
                    <p style='text-align: justify;'>Bienvenidos a la aplicación de estadísticas de voleibol profesional. 
                    Aquí encontrarás información detallada sobre diferentes equipos de voleibol, jugadores destacados,
                    estadísticas de partidos y más. Explora las secciones y disfruta de la experiencia.</p>
                </div>
            """
            st.markdown(presentacion, unsafe_allow_html=True)

            
            script_directory = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_directory, 'data', 'Equipos_final.csv')
            df = pd.read_csv(csv_path)

            equipos_a_imagenes = {
                                    'Arenal Emeve': 'https://yt3.googleusercontent.com/ytc/APkrFKYFDxQgjP4QpTyT4l0USR9bKOXH3EjYE54gcVIn8Q=s900-c-k-c0x00ffffff-no-rj',
                                    'Cisneros Alter': 'https://pbs.twimg.com/profile_images/1715679951054049280/yiauFOvS_400x400.jpg',
                                    'Manacor':'https://voleimanacor.club/wp-content/uploads/2018/08/logonouok.png',
                                    'Guaguas': 'https://clubvoleibolguaguas.com/wp-content/uploads/2023/06/Logo-CV-Guaguas-250px.png',
                                    'CV Melilla':'https://static.flashscore.com/res/image/data/AqSNrktr-IFY3e7TS.png',
                                    'CV San Roque':'https://clubvoleibolguaguas.com/wp-content/uploads/2023/07/CV-San-Roque-Batan-1269x1280.png',
                                    'Rio Duero Soria':'https://www.rioduerovoley.com/wp-content/uploads/2021/08/cropped-Rio-Duero-TRANPARENTE-HA.png',
                                    'CV Teruel' : 'https://i0.wp.com/sextoanillo.com/wp-content/uploads/2022/08/descarga.png?fit=225%2C225&ssl=1',
                                    'Unicaja Almeria':'https://assets.hypefactors.com/companies/company-logos/cropped/QJKKL8VujtUbZ85DgfAs1voJqcxmAETmsiSyyImF.png',
                                    'Conqueridor Valencia':'https://plazadeportiva.valenciaplaza.com/public/Image/2022/7/logo-fondogris_NoticiaAmpliada.jpg',
                                    'CV Villena Petrer':'https://www.comunitatdelesport.com/wp-content/uploads/2021/11/Voley-Petrer.jpg',
                                    'Barca Voleibol': 'https://volleybox.net/media/upload/teams/1426198410Slzl4.png',
                                    'Rotogal Boiro':'https://boirovoleibol.com/wp-content/uploads/2021/11/logotipo-VOLEIBOL.fw_.w114px.png',
                                    'Voley Textil Santanderina':'https://www.rfevb.com/hanImgNot.ashx?src=Logo%20Club-imgEs20221029085114.png&fol=N&Post=Sli',
                                    'Intasa':'https://i0.wp.com/sextoanillo.com/wp-content/uploads/2021/10/sansadurninho.png?fit=363%2C363&ssl=1',
                                    'Ibiza Voley':'https://ibi.gsstatic.es/sfAttachPlugin/959745.jpg',
                                    'Grau':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTA2PH549w2uNdqAaIVg8QzocaiHmL7WCvPayz9z_Pfqz_yJeDgXWe6o-SK_9bytyIitwk&usqp=CAU',
                                    'Voleibol Almoradi':'https://intranet.rfevb.com/clubes/logos/web/cl00130.png',
                                    'Vecindario Las Palmas':'https://scontent-mad1-1.xx.fbcdn.net/v/t39.30808-6/300565570_524083349522452_5874749077301041614_n.png?_nc_cat=106&ccb=1-7&_nc_sid=efb6e6&_nc_ohc=9wl7dNNOTC0AX85EBcS&_nc_ht=scontent-mad1-1.xx&oh=00_AfB6Q31hGxtM38yaHxqkUHo8zACQz4hr62POjsrpit65ZQ&oe=6572E458',   
                                    'Voley Palma': 'https://static.wixstatic.com/media/a88496_ff1acd3ead504b2889816d01bd63b2c3~mv2.jpeg/v1/fit/w_2500,h_1330,al_c/a88496_ff1acd3ead504b2889816d01bd63b2c3~mv2.jpeg'
            }
            equipo_seleccionado = st.sidebar.selectbox('', ['Seleccione un equipo'] + list(df.Equipo))

            if equipo_seleccionado in equipos_a_imagenes:
                url_imagen = equipos_a_imagenes[equipo_seleccionado]
                self._show_image_and_info(equipo_seleccionado, url_imagen)
            else:
                st.sidebar.warning("Seleccione un equipo para más información.")



            st.markdown('<div class="header-styles">Información de temporada</div>', unsafe_allow_html=True)


            #Fuera del sidebar:
            
            query_jornadas = "SELECT fecha,hora,equipo_local, resultado, equipo_visitante FROM jornadas"
            resultados_jornadas = self.ejecutar_consulta(query_jornadas)
            print("Tipo de resultados_jornadas:", type(resultados_jornadas))
            equipos_unicos = resultados_jornadas['equipo_local'].unique()

            # Widget para seleccionar el equipo por el cual filtrar
            equipo_filtro = st.selectbox("Selecciona equipo para filtrar", ['Todos'] + list(equipos_unicos))

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Tabla de jornadas")
                
            
                if equipo_filtro != 'Todos':
                    resultados_jornadas = resultados_jornadas[
                        (resultados_jornadas['equipo_local'] == equipo_filtro) | (resultados_jornadas['equipo_visitante'] == equipo_filtro)]

                
                if resultados_jornadas is not None and not resultados_jornadas.empty:
                    nombres_encabezados = ['Fecha','Hora','Equipo Local', 'Resultado', 'Equipo Visitante']
                    fig_jornadas = go.Figure(data=[go.Table(
                        header=dict(values = nombres_encabezados,
                                    fill_color='#FF4B4B',  # Color de fondo del encabezado
                                    align='center',
                                    font=dict(color='white', size=16)),  # Color y tamaño de la fuente del encabezado
                        cells=dict(values=[resultados_jornadas[col] for col in resultados_jornadas.columns],
                                fill_color='#F0F2F6',  # Color de fondo de las celdas
                                align='center',
                                font=dict(color='#2C3E50', size=14)))  # Color y tamaño de la fuente de las celdas
                    ])
                    st.plotly_chart(fig_jornadas, use_container_width=True)
                    

            
            
            with col2:
                st.subheader("Tabla de posiciones")

                
                resultados_filtrados_clasificacion = self.ejecutar_consulta("SELECT posicion,equipo,pj,p,g,pts FROM clasificacion WHERE temporada='2023-2024'")

                
                if resultados_filtrados_clasificacion is not None and not resultados_filtrados_clasificacion.empty:
                    
                    nombres_encabezados = ['Posición', 'Equipo', 'Partidos Jugados', 'Partidos Perdidos', 'Partidos Ganados', 'PTS']

                    fig_clasificacion = go.Figure(data=[go.Table(
                        header=dict(values=nombres_encabezados,
                                    fill_color='#FF4B4B',  # Color de fondo del encabezado
                                    align='center',
                                    font=dict(color='white', size=16)),  # Color y tamaño de la fuente del encabezado
                        cells=dict(values=[resultados_filtrados_clasificacion[col] for col in resultados_filtrados_clasificacion.columns],
                                fill_color='#F0F2F6',  # Color de fondo de las celdas
                                align='center',
                                font=dict(color='#2C3E50', size=14)))  # Color y tamaño de la fuente de las celdas
                    ])
                    st.plotly_chart(fig_clasificacion, use_container_width=True)

            
            query = "SELECT posicion, equipo FROM clasificacion WHERE temporada='2023-2024'"
            data = self.ejecutar_consulta(query)
            df = pd.DataFrame(data)

            
            fig_barras = px.bar(df, x="posicion", y="equipo", title="Posiciones por equipo")
            fig_barras.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_barras, use_container_width=True)

            col1, col2 = st.sidebar.columns(2)
            with col1:
                # logo para cuenta personal
                github_logo = "https://icon-library.com/images/github-logo-icon/github-logo-icon-12.jpg"
                github_link = f'<a href="https://github.com/AlejandroCasna"><img src="{github_logo}" width="50"></a>'
                st.sidebar.markdown(github_link, unsafe_allow_html=True)
            with col2:
                linkedin_logo = "https://www.freeiconspng.com/thumbs/linkedin-logo-png/linkedin-logo-0.png"
                linkedin_link = f'<a href="https://www.linkedin.com/in/alejandrocasna/"><img src="{linkedin_logo}" width="50"></a>'
                st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)

        def estadisticas_equipos(self):
            self._set_background("https://integralspor.com/uploads/blog/detail/1618e792d4b1254221.jpg")
            self._set_header_style("#FF4B4B", "rgba(0,0,0,0.2)")

            st.markdown('<div class="header-styles">Estadísticas de Equipo</div>', unsafe_allow_html=True)

            query_temporadas = "SELECT DISTINCT temporada FROM estadistica"
            temporadas_disponibles = self.ejecutar_consulta(query_temporadas)['temporada'].unique()

            
            temporada_seleccionada = st.selectbox('Selecciona la temporada', temporadas_disponibles)

            
            query_jornadas = f"SELECT * FROM estadistica WHERE temporada = '{temporada_seleccionada}'"
            resultados_jornadas = self.ejecutar_consulta(query_jornadas)

            mapeo_nombres_columnas = {
                                    'jugados': 'Partidos Jugados',
                                    'sets_jugados': 'Sets Jugados',
                                    'total_puntos': 'Total de Puntos',
                                    'break_puntos': 'Break Puntos',
                                    'puntos_ganados': 'Puntos Ganados',
                                    'puntos_perdidos': 'Puntos Perdidos',
                                    'total_saque': 'Total de Saques',
                                    'puntos_saque': 'Puntos de Saque',
                                    'error_saque': 'Errores de Saque',
                                    'puntos_por_set_saque': 'Puntos de Saque por set',
                                    'efic_saque': 'Eficiencia de Saque',
                                    'total_recepcion': 'Total Recepciones',
                                    'error_recepcion': 'Errores de Recepcion',
                                    'negativo_recepcion': 'Recepcion Negativa',
                                    'positivo_recepcion': 'Recepcion Positiva',
                                    'excelente_recepcion': 'Doble Positiva',
                                    'efic_recepcion': 'Eficiencia de Recepcion',
                                    'total_ataque': 'Total de Ataques',
                                    'error_ataque': 'Error Ataques',
                                    'ataque_bloqueado': 'Ataques Bloquedos',
                                    'positivo_ataque': 'Ataque Positivo',
                                    'excelente_ataque': 'Punto de Ataque',
                                    'efic_ataque': 'Efectividad Ataque ',
                                    'toque_red_bloqueo': 'Toque red del Bloqueo',
                                    'puntos_de_bloqueo': 'Ataque Bloqueado',
                                    'puntos_set_bloqueo': 'Ataque Bloqueado por set',}
                                    
            


            if resultados_jornadas is not None and not resultados_jornadas.empty:
                resultados_jornadas_renombrado = resultados_jornadas.copy()
                resultados_jornadas_renombrado.columns = [mapeo_nombres_columnas.get(col.lower(), col) for col in resultados_jornadas_renombrado.columns]
                equipo_seleccionado = st.selectbox('Selecciona un equipo', resultados_jornadas_renombrado['equipo'].unique())
                
                
                tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Radar', 'Barras Apiladas','Pastel'], key="grafico_selector")

                columnas_a_mostrar = [col for col in resultados_jornadas_renombrado.columns if col not in ['equipo', 'id_equipo', 'temporada']]

                columnas_disponibles = st.multiselect('Selecciona las columnas', columnas_a_mostrar)

                if columnas_disponibles:
                    helper_graficos = Graficos(resultados_jornadas_renombrado)

                    if equipo_seleccionado:
                        if tipo_grafico == 'Radar':
                            helper_graficos.crear_grafico_arana(equipo_seleccionado, columnas_disponibles)
                        elif tipo_grafico == 'Barras Apiladas':
                            helper_graficos.grafico_barras_apiladas(equipo_seleccionado, columnas_disponibles)
                        elif tipo_grafico=='Pastel':
                            helper_graficos.grafico_pastel(equipo_seleccionado, columnas_disponibles)

                        else:
                            st.warning('Tipo de gráfico no válido.')
                    else:
                        st.warning('Selecciona un equipo para visualizar el gráfico.')





                st.markdown('<div class="header-styles">Comparación de Temporadas</div>', unsafe_allow_html=True)

                
                todas_temporadas = self.ejecutar_consulta("SELECT DISTINCT temporada FROM estadistica")['temporada'].unique()

                
                temporadas_a_comparar = st.multiselect('Selecciona las temporadas para comparar', todas_temporadas)

                if temporadas_a_comparar:
                    if len(temporadas_a_comparar) == 2:
                        query_temporadas = f"SELECT * FROM estadistica WHERE temporada IN {tuple(temporadas_a_comparar)}"
                        resultados_temporadas = self.ejecutar_consulta(query_temporadas)

                        if resultados_temporadas is not None and not resultados_temporadas.empty:
                            resultados_temporadas_renombrado = resultados_temporadas.copy()
                            resultados_temporadas_renombrado.columns = [mapeo_nombres_columnas.get(col.lower(), col) for col in resultados_temporadas_renombrado.columns]

                        
                            equipo_seleccionado_temporadas = st.selectbox('Selecciona un equipo', resultados_temporadas_renombrado['equipo'].unique())

                            
                            tipo_grafico_temporadas = st.selectbox('Selecciona el tipo de gráfico', ['Radar', 'Barras Apiladas'], key="grafico_temporadas_selector")

                            columnas_a_mostrar_temporadas = [col for col in resultados_temporadas_renombrado.columns if col not in ['equipo', 'id_equipo', 'temporada']]

                            columnas_disponibles_temporadas = st.multiselect('Selecciona las columnas', columnas_a_mostrar_temporadas, key="grafico_selector2")

                            if columnas_disponibles_temporadas:
                                helper_graficos_temporadas = Graficos(resultados_temporadas_renombrado)

                                if equipo_seleccionado_temporadas:
                                    if tipo_grafico_temporadas == 'Radar':
                                        helper_graficos_temporadas.grafico_arana_multiple(temporadas_a_comparar, equipo_seleccionado_temporadas, columnas_disponibles_temporadas)
                                    elif tipo_grafico_temporadas == 'Barras Apiladas':
                                        helper_graficos_temporadas.grafico_barras_apiladas(equipo_seleccionado_temporadas, columnas_disponibles_temporadas)
                                    else:
                                        st.warning('Tipo de gráfico no válido.')
                                else:
                                    st.warning('Selecciona un equipo para visualizar el gráfico.')
                    else:
                        st.warning('Selecciona al menos dos temporada para comparar.')



            
        
            st.markdown('<div class="header-styles">Comparación de Equipos</div>', unsafe_allow_html=True)

            todos_equipos = self.ejecutar_consulta("SELECT DISTINCT equipo FROM estadistica")['equipo'].unique()

            
            equipos_seleccionados = st.multiselect('Selecciona los equipos (máximo 2)', todos_equipos, default=[])
            if len(equipos_seleccionados) == 2:
                
                query_temporadas_equipos = f"SELECT DISTINCT temporada FROM estadistica WHERE equipo IN {tuple(equipos_seleccionados)}"
                temporadas_disponibles_equipos = self.ejecutar_consulta(query_temporadas_equipos)['temporada'].unique()
            
                if temporadas_disponibles_equipos.any():  
                    
                    temporadas_equipo1 = self.ejecutar_consulta(f"SELECT DISTINCT temporada FROM estadistica WHERE equipo = '{equipos_seleccionados[0]}'")['temporada'].unique()
                    temporadas_equipo2 = self.ejecutar_consulta(f"SELECT DISTINCT temporada FROM estadistica WHERE equipo = '{equipos_seleccionados[1]}'")['temporada'].unique()
                    temporadas_comunes = set(temporadas_equipo1) & set(temporadas_equipo2)
                    temporada_seleccionada_equipos = st.selectbox('Selecciona la temporada', temporadas_comunes, key="temporada_selector_equipos")

                    
                    tipo_grafico_equipos = st.selectbox('Selecciona el tipo de gráfico', ['Radar', 'Barras Apiladas'], key="grafico_equipos_selector")

                    
                    columnas_a_mostrar_equipos = st.multiselect('Selecciona las columnas', mapeo_nombres_columnas.values(), key="grafico_selector_equipos")

                    if temporada_seleccionada_equipos and tipo_grafico_equipos and columnas_a_mostrar_equipos:
                        
                        query_equipos = f"SELECT * FROM estadistica WHERE temporada = '{temporada_seleccionada_equipos}' AND equipo IN {tuple(equipos_seleccionados)}"
                        resultados_equipos = self.ejecutar_consulta(query_equipos)

                        if resultados_equipos is not None and not resultados_equipos.empty:
                            resultados_equipos_renombrado = resultados_equipos.copy()
                            resultados_equipos_renombrado.columns = [mapeo_nombres_columnas.get(col.lower(), col) for col in resultados_equipos_renombrado.columns]

                            helper_graficos_equipos = Graficos(resultados_equipos_renombrado)

                            
                            if tipo_grafico_equipos == 'Radar':
                                helper_graficos_equipos.grafico_arana_multiple_equipo([temporada_seleccionada_equipos], equipos_seleccionados, columnas_a_mostrar_equipos)
                            elif tipo_grafico_equipos == 'Barras Apiladas':
                                helper_graficos_equipos.grafico_barras_equipo_multiple([temporada_seleccionada_equipos], equipos_seleccionados, columnas_a_mostrar_equipos)
                            else:
                                st.warning('Tipo de gráfico no válido.')
                        else:
                            st.warning('No se pudieron obtener los datos para la temporada y equipos seleccionados.')
                else:
                    st.warning('No hay temporadas disponibles para los equipos seleccionados.')
            else:
                st.warning('Selecciona al menos un equipo para continuar.')



            col1, col2 = st.sidebar.columns(2)
            with col1:
                # logo para cuenta personal
                github_logo = "https://icon-library.com/images/github-logo-icon/github-logo-icon-12.jpg"
                github_link = f'<a href="https://github.com/AlejandroCasna"><img src="{github_logo}" width="50"></a>'
                st.sidebar.markdown(github_link, unsafe_allow_html=True)
            with col2:
                linkedin_logo = "https://www.freeiconspng.com/thumbs/linkedin-logo-png/linkedin-logo-0.png"
                linkedin_link = f'<a href="https://www.linkedin.com/in/alejandrocasna/"><img src="{linkedin_logo}" width="50"></a>'
                st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)

        def estadisticas_jugadores(self):
            self._set_background("https://integralspor.com/uploads/blog/detail/1618e792d4b1254221.jpg")
            self._set_header_style("#FF4B4B", "rgba(0,0,0,0.2)")

            st.markdown('<div class="header-styles">Estadísticas Jugadores</div>', unsafe_allow_html=True)

            query_temporadas = "SELECT DISTINCT temporada FROM estadistica"
            temporadas_disponibles = self.ejecutar_consulta(query_temporadas)['temporada'].unique()
            posiciones = ('Central', 'Libero', 'Opuesto', 'Colocador', 'Receptor/Punta/Ala')
            posicion_seleccionada = st.selectbox('Seleccione la Posición Deseada', posiciones)
            temporada_seleccionada = st.selectbox('Selecciona la temporada', temporadas_disponibles)

            if temporada_seleccionada == '2023-2024':
                query_jugadores = "SELECT * FROM central WHERE temporada='2022-2023'"
                jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                if jugadores_seleccionados and columnas_a_mostrar:
                    tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                    graficos = Graficos(jugadores_disponibles)

                    if tipo_grafico == 'Dona':
                        graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                    elif tipo_grafico == 'Araña':
                        graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                        
                elif temporada_seleccionada == '2022-2023':
                    query_jugadores = "SELECT * FROM central WHERE temporada='2022-2023'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                    
                elif temporada_seleccionada == '2021-2022':
                    query_jugadores = "SELECT * FROM central WHERE temporada='2021-2022'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2020-2021':
                    query_jugadores = "SELECT * FROM central WHERE temporada='2020-2021'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                
                elif temporada_seleccionada == '2019-2020':
                    query_jugadores = "SELECT * FROM central WHERE temporada='2019-2020'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                else:
                    pass
                
            elif posicion_seleccionada == 'Libero':
                if temporada_seleccionada == '2023-2024':
                    query_jugadores = "SELECT * FROM libero WHERE temporada='2023-2024'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2022-2023':
                    query_jugadores = "SELECT * FROM libero WHERE temporada='2022-2023'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2021-2022':
                    query_jugadores = "SELECT * FROM libero WHERE temporada='2021-2022'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2020-2021':
                    query_jugadores = "SELECT * FROM libero WHERE temporada='2020-2021'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2019-2020':
                    query_jugadores = "SELECT * FROM libero WHERE temporada='2019-2020'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                else:
                    pass

            elif posicion_seleccionada == 'Opuesto':
                if temporada_seleccionada == '2023-2024':
                    query_jugadores = "SELECT * FROM opuesto WHERE temporada='2023-2024'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2022-2023':
                    query_jugadores = "SELECT * FROM opuesto WHERE temporada='2022-2023'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2021-2022':
                    query_jugadores = "SELECT * FROM opuesto WHERE temporada='2021-2022'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2020-2021':
                    query_jugadores = "SELECT * FROM opuesto WHERE temporada='2020-2021'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2019-2020':
                    query_jugadores = "SELECT * FROM opuesto WHERE temporada='2019-2020'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                else:
                    pass

            elif posicion_seleccionada == 'Colocador':
                if temporada_seleccionada == '2023-2024':
                    query_jugadores = "SELECT * FROM colocador WHERE temporada='2023-2024'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2022-2023':
                    query_jugadores = "SELECT * FROM colocador WHERE temporada='2022-2023'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                    
                elif temporada_seleccionada == '2021-2022':
                    query_jugadores = "SELECT * FROM colocador WHERE temporada='2021-2022'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2020-2021':
                    query_jugadores = "SELECT * FROM colocador WHERE temporada='2020-2021'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2019-2020':
                    query_jugadores = "SELECT * FROM colocador WHERE temporada='2019-2020'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                else:
                    pass

            elif posicion_seleccionada == 'Receptor/Punta/Ala':
                if temporada_seleccionada == '2023-2024':
                    query_jugadores = "SELECT * FROM receptor WHERE temporada='2023-2024'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2022-2023':
                    query_jugadores = "SELECT * FROM receptor WHERE temporada='2022-2023'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2021-2022':
                    query_jugadores = "SELECT * FROM receptor WHERE temporada='2021-2022'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2020-2021':
                    query_jugadores = "SELECT * FROM receptor WHERE temporada='2020-2021'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)

                elif temporada_seleccionada == '2019-2020':
                    query_jugadores = "SELECT * FROM receptor WHERE temporada='2019-2020'"
                    jugadores_disponibles = self.ejecutar_consulta(query_jugadores)
                    jugadores_seleccionados = st.multiselect('Selecciona jugadores', jugadores_disponibles['nombre'].unique())
                    columnas_a_mostrar = st.multiselect('Selecciona las columnas para el gráfico', jugadores_disponibles.columns)

                    if jugadores_seleccionados and columnas_a_mostrar:
                        tipo_grafico = st.selectbox('Selecciona el tipo de gráfico', ['Dona', 'Araña'])
                        graficos = Graficos(jugadores_disponibles)

                        if tipo_grafico == 'Dona':
                            graficos.grafico_dona_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                        elif tipo_grafico == 'Araña':
                            graficos.grafico_arana_jugador(jugadores_disponibles, jugadores_seleccionados, columnas_a_mostrar)
                else:
                    pass

            else:
                pass

            col1, col2 = st.sidebar.columns(2)
            with col1:
                # logo para cuenta personal
                github_logo = "https://icon-library.com/images/github-logo-icon/github-logo-icon-12.jpg"
                github_link = f'<a href="https://github.com/AlejandroCasna"><img src="{github_logo}" width="50"></a>'
                st.sidebar.markdown(github_link, unsafe_allow_html=True)
            with col2:
                linkedin_logo = "https://www.freeiconspng.com/thumbs/linkedin-logo-png/linkedin-logo-0.png"
                linkedin_link = f'<a href="https://www.linkedin.com/in/alejandrocasna/"><img src="{linkedin_logo}" width="50"></a>'
                st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
            


    app = VoleyStatsApp()

    # Mostrar la barra lateral y la página seleccionada
    pagina_seleccionada = st.sidebar.radio("Selecciona una página", ["Inicio", "Estadísticas Equipos", "Estadísticas Jugadores"])


    if pagina_seleccionada == "Inicio":
        app.pagina_inicio()
    elif pagina_seleccionada == "Estadísticas Equipos":
        app.estadisticas_equipos()
    elif pagina_seleccionada == "Estadísticas Jugadores":
        app.estadisticas_jugadores()

elif user_input != "" and user_input != contrasenia:
    st.error("Contraseña incorrecta. Por favor, intenta nuevamente.")