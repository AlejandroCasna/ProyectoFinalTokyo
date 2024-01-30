import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


class Graficos:

    def __init__(self, df):
        self.df = df

    def grafico_barras_apiladas(self, equipo, columnas_seleccionadas):
        df_selected_team = self.df[self.df['equipo'] == equipo]
        df_selected_columns = df_selected_team[['equipo', 'temporada'] + columnas_seleccionadas]
        df_long = df_selected_columns.melt(id_vars=['equipo', 'temporada'], var_name='Estadística', value_name='Valor')
        fig = px.bar(df_long, x='Estadística', y='Valor', color='temporada', title=f"Estadísticas de {equipo}", barmode='stack', orientation='v')

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.2)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=20, color='black'),
            title_font=dict(size=30, color='black'),
            legend_title_font=dict(size=30, color='white'),
            legend_font=dict(size=20, color='black'),
            width=800,  
            margin=dict(l=0, r=0, b=0, t=50),  
        )
        for trace in fig.data:
            trace.update(text=trace.y, textposition='inside') # type: ignore

        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True)

    def crear_grafico_arana(self, equipo, columnas_seleccionadas):
        df_selected_team = self.df[self.df['equipo'] == equipo]
        df_selected_columns = df_selected_team[['equipo'] + columnas_seleccionadas]
        df_melt = pd.melt(df_selected_columns, id_vars=['equipo'], var_name='theta', value_name='r')

        fig = px.line_polar(df_melt, r='r', theta='theta', line_close=True, color='equipo', line_group='equipo')
        fig.update_traces(fill='toself')

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.6)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(size=20, color='black'),
            legend=dict(
                x=1,
                y=1,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='Black',
                borderwidth=1,
                font=dict(
                    size=14,
                    color='black'
                )
            ),
            title=dict(
                text='Estadísticas de Equipo',
                x=0,
                y=0.95,
                xanchor='left',
                yanchor='top',
                font=dict(size=20, color='black')
            )
        )

        fig.update_polars(
            angularaxis=dict(
                tickfont=dict(size=20, color='black'),
                linecolor='black',
            ),
            radialaxis=dict(
                tickfont=dict(size=20, color='black'),
                linecolor='black',
            ),
        )

        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True)

    def grafico_pastel(self, equipo, columnas_seleccionadas):
        df_selected_team = self.df[self.df['equipo'] == equipo]
        df_selected_columns = df_selected_team[['equipo', 'temporada'] + columnas_seleccionadas]
        df_long = df_selected_columns.melt(id_vars=['equipo', 'temporada'], var_name='Estadística', value_name='Valor')

        fig = px.sunburst(df_long, path=['temporada', 'Estadística'], values='Valor', title=f"Estadísticas de {equipo}")

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.2)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=20, color='black'),
            title_font=dict(size=30, color='black'),
            legend_title_font=dict(size=30, color='white'),
            legend_font=dict(size=20, color='black'),
            width=800,  
            margin=dict(l=0, r=0, b=0, t=50),  
        )
        fig.update_traces(insidetextorientation='radial', textinfo='label+percent entry')  
        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True)

    def grafico_dona(self, equipo, columnas_seleccionadas):
        df_selected_team = self.df[self.df['equipo'] == equipo]
        df_selected_columns = df_selected_team[['equipo', 'temporada'] + columnas_seleccionadas]
        df_long = df_selected_columns.melt(id_vars=['equipo', 'temporada'], var_name='Estadística', value_name='Valor')

        fig = px.pie(df_long, names='temporada', values='Valor', title=f"Estadísticas de {equipo}", hole=0.4)

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.2)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=20, color='black'),
            title_font=dict(size=30, color='black'),
            legend_title_font=dict(size=30, color='white'),
            legend_font=dict(size=20, color='black'),
            width=800,  
            margin=dict(l=0, r=0, b=0, t=50),  
        )

        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True)
    
    def grafico_barras_apiladas_multiple(self, temporadas_seleccionadas, equipo, columnas_seleccionadas):
        resultados_equipo_temporadas = []
        for temporada in temporadas_seleccionadas:
            # Modificamos esto para acceder directamente a los resultados proporcionados
            query = f"temporada == '{temporada}' and equipo == @equipo"
            resultados_temporada = self.df.query(query, local_dict={'equipo': equipo})
            
            if not resultados_temporada.empty:
                resultados_equipo_temporadas.append(resultados_temporada)

        if resultados_equipo_temporadas:
            df_selected_columns = pd.concat([temp_df[['temporada'] + columnas_seleccionadas] for temp_df in resultados_equipo_temporadas])
            df_long = df_selected_columns.melt(id_vars=['temporada'], var_name='Estadística', value_name='Valor')

            fig = px.bar(df_long, x='Estadística', y='Valor', color='temporada',
                        title=f"Estadísticas de {equipo} - Temporadas Comparadas",
                        barmode='stack', orientation='v').update_traces(text=df_long['Valor'], textposition='inside').data[0]

            fig.update_traces(text=df_long['Valor'], textposition='inside') # type: ignore

            fig.update_layout( # type: ignore
                paper_bgcolor='rgba(255,255,255,0.2)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(size=20, color='black'),
                title_font=dict(size=30, color='black'),
                legend_title_font=dict(size=30, color='white'),
                legend_font=dict(size=20, color='black'),
                width=800,  
                margin=dict(l=0, r=0, b=0, t=50),  
            )

            
            espacio_en_blanco = st.empty()
            espacio_en_blanco.plotly_chart(fig[0], use_container_width=True)
        else:
            st.warning(f"No hay datos disponibles para el equipo '{equipo}' y las temporadas seleccionadas.")

    def grafico_arana_multiple(self, temporadas_seleccionadas, equipo, columnas_seleccionadas):
        resultados_equipo_temporadas = []
        
        for temporada in temporadas_seleccionadas:
            # Modificamos esto para acceder directamente a los resultados proporcionados
            query = f"temporada == '{temporada}' and equipo == @equipo"
            resultados_temporada = self.df.query(query, local_dict={'equipo': equipo})
            
            if not resultados_temporada.empty:
                resultados_equipo_temporadas.append(resultados_temporada)

        if resultados_equipo_temporadas:
            df_selected_columns = pd.concat([temp_df[['temporada'] + columnas_seleccionadas] for temp_df in resultados_equipo_temporadas])
            df_long = df_selected_columns.melt(id_vars=['temporada'], var_name='Estadística', value_name='Valor')

            fig = px.line_polar(df_long, r='Valor', theta='Estadística', color='temporada',
                                line_close=True, range_r=[0, df_long['Valor'].max()],
                                title=f"Estadísticas de {equipo} - Temporadas Comparadas")

            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0.6)',
                plot_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=20, color='black'),
                width=800,  
                margin=dict(l=0, r=0, b=0, t=50),  
                legend=dict(
                    x=1,
                    y=1,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='Black',
                    borderwidth=1,
                    font=dict(
                        size=14,
                        color='black'
                    )
                ),
                title=dict(
                    text='Estadísticas de Equipo',
                    x=0,
                    y=0.95,
                    xanchor='left',
                    yanchor='top',
                    font=dict(size=20, color='black')
                )
            )

            fig.update_polars(
                angularaxis=dict(
                    tickfont=dict(size=20, color='black'),
                    linecolor='black',
                ),
                radialaxis=dict(
                    tickfont=dict(size=20, color='black'),
                    linecolor='black',
                ),
            )

            espacio_en_blanco = st.empty()
            espacio_en_blanco.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No hay datos disponibles para las temporadas seleccionadas.")

    def grafico_arana_multiple_equipo(self, temporadas_seleccionadas, equipos_seleccionados, columnas_seleccionadas):
        resultados_equipos_temporadas = []

        for equipo in equipos_seleccionados:
            for temporada in temporadas_seleccionadas:
                query = f"temporada == '{temporada}' and equipo == @equipo"
                resultados_temporada = self.df.query(query, local_dict={'equipo': equipo})

                if not resultados_temporada.empty:
                    resultados_equipos_temporadas.append(resultados_temporada)

        if resultados_equipos_temporadas:
            df_selected_columns = pd.concat([temp_df[['temporada', 'equipo'] + columnas_seleccionadas] for temp_df in resultados_equipos_temporadas])
            df_long = df_selected_columns.melt(id_vars=['temporada', 'equipo'], var_name='Estadística', value_name='Valor')

            fig = px.line_polar(df_long, r='Valor', theta='Estadística', color='equipo',
                                line_close=True, range_r=[0, df_long['Valor'].max()],
                                title=f"Comparación de Equipos - Temporadas: {', '.join(temporadas_seleccionadas)}")

            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0.6)',
                plot_bgcolor='rgba(255,255,255,0.9)',
                font=dict(size=20, color='black'),
                width=800,  
                margin=dict(l=0, r=0, b=0, t=50),  
                legend=dict(
                    x=1,
                    y=1,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='Black',
                    borderwidth=1,
                    font=dict(
                        size=14,
                        color='black'
                    )
                ),
                title=dict(
                    text='Comparación de Equipos',
                    x=0,
                    y=0.95,
                    xanchor='left',
                    yanchor='top',
                    font=dict(size=20, color='black')
                )
            )

            fig.update_polars(
                angularaxis=dict(
                    tickfont=dict(size=20, color='black'),
                    linecolor='black',
                ),
                radialaxis=dict(
                    tickfont=dict(size=20, color='black'),
                    linecolor='black',
                ),
            )

            espacio_en_blanco = st.empty()
            espacio_en_blanco.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No hay datos disponibles para las temporadas y equipos seleccionados.")

    def grafico_barras_equipo_multiple(self, temporadas_seleccionadas, equipos_seleccionados, columnas_seleccionadas):
        resultados_equipos_temporadas = []

        for equipo in equipos_seleccionados:
            for temporada in temporadas_seleccionadas:
                query = f"temporada == '{temporada}' and equipo == @equipo"
                resultados_temporada = self.df.query(query, local_dict={'equipo': equipo})

                if not resultados_temporada.empty:
                    resultados_equipos_temporadas.append(resultados_temporada)

        if resultados_equipos_temporadas:
            df_selected_columns = pd.concat([temp_df[['temporada', 'equipo'] + columnas_seleccionadas] for temp_df in resultados_equipos_temporadas])
            df_long = df_selected_columns.melt(id_vars=['temporada', 'equipo'], var_name='Estadística', value_name='Valor')

            fig = px.bar(df_long, x='Estadística', y='Valor', color='equipo',
                        title=f"Comparación de Equipos - Temporadas: {', '.join(temporadas_seleccionadas)}",
                        barmode='stack', orientation='v')

            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0.2)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(size=20, color='black'),
                title_font=dict(size=30, color='black'),
                legend_title_font=dict(size=30, color='white'),
                legend_font=dict(size=20, color='black'),
                width=800,  
                margin=dict(l=0, r=0, b=0, t=50),  
            )

            espacio_en_blanco = st.empty()
            espacio_en_blanco.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No hay datos disponibles para las temporadas y equipos seleccionados.")

    def grafico_dona_jugador(self,df, jugadores_seleccionados, columnas_seleccionadas):
        df_selected_players = df[df['nombre'].isin(jugadores_seleccionados)][['nombre'] + columnas_seleccionadas]
        df_long = df_selected_players.melt(id_vars=['nombre'], var_name='Estadística', value_name='Valor')

        
        df_long['Etiqueta'] = df_long['nombre'] + ' - ' + df_long['Estadística']

        fig = go.Figure(go.Pie(
            labels=df_long['Etiqueta'],
            values=df_long['Valor'],
            hole=0.4,
            hoverinfo='label+percent+value',
            
        ))

        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.2)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=20, color='black'),
            title_font=dict(size=30, color='black'),
            title=f"Estadísticas de Jugadores",
            legend_title_font=dict(size=30, color='white'),
            legend_font=dict(size=20, color='black'),
            width=800,
            margin=dict(l=0, r=0, b=0, t=50),
        )

        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True) 

    def grafico_arana_jugador(self, df, jugadores_seleccionados, columnas_seleccionadas):
        df_selected_players = df[df['nombre'].isin(jugadores_seleccionados)][['nombre'] + columnas_seleccionadas]
        df_long = df_selected_players.melt(id_vars=['nombre'], var_name='Estadística', value_name='Valor')

        fig = px.line_polar(df_long, r='Valor', theta='Estadística', color='nombre',
                            line_close=True, range_r=[0, df_long['Valor'].max()],
                            title=f"Estadísticas de Jugadores - Temporada 2023-2024")

        # Restablecer el diseño y configurar otros ajustes según sea necesario
        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,0.6)',
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(size=20, color='black'),
            legend=dict(
                x=1,
                y=1,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='Black',
                borderwidth=1,
                font=dict(
                    size=14,
                    color='black'
                )
            ),
            title=dict(
                text='Estadísticas de Jugadores',
                x=0,
                y=0.95,
                xanchor='left',
                yanchor='top',
                font=dict(size=20, color='black')
            ),
            # Centrar el gráfico en el contenedor
            width=800,
            margin=dict(l=0, r=0, b=0, t=50),
        )

        # Mostrar el gráfico centrado dentro del espacio en blanco
        espacio_en_blanco = st.empty()
        espacio_en_blanco.plotly_chart(fig, use_container_width=True)   