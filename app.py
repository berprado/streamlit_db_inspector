# Streamlit app to inspect database schema
"""
Streamlit app to inspect database schema.
This app allows users to load and inspect the structure of tables in a database.
It provides a user interface to select a table and view its structure.
"""
import streamlit as st
import pandas as pd
try:
    from db_utils import get_tables, get_table_structure, get_table_full_info
except ImportError:
    st.error("❌ Error: No se pudo importar el módulo 'db_utils'. Asegúrese de que el archivo 'db_utils.py' existe y contiene las funciones necesarias.")
    st.stop()

st.set_page_config(
    page_title="DB Schema Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .table-header {
        font-weight: bold;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .metadata-card {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #4e8cff;
    }
    .constraint-card {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 8px;
        border-left: 3px solid #0068c9;
        color: #333333;  /* Color de texto oscuro para mejor contraste */
    }
    .code-block {
        background-color: #272822;
        padding: 15px;
        border-radius: 5px;
        color: #f8f8f2;
        overflow-x: auto;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .badge {
        font-size: 0.8em;
        padding: 3px 8px;
        border-radius: 10px;
        color: white;
        display: inline-block;
        margin-right: 5px;
    }
    .badge-primary {
        background-color: #0068c9;
    }
    .badge-secondary {
        background-color: #6c757d;
    }
    .badge-success {
        background-color: #198754;
    }
    /* Estilos mejorados para las tarjetas de claves foráneas */
    .fk-card {
        background-color: #eef7ff;  /* Fondo más claro para mejor contraste */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 8px;
        border-left: 3px solid #0068c9;
        color: #333333;  /* Color de texto oscuro para mejor contraste */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    /* Estilos mejorados para las tarjetas de índices */
    .index-card {
        background-color: #f2f8f2;  /* Color distinto para diferenciar de las FK */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 8px;
        border-left: 3px solid #198754;
        color: #333333;  /* Color de texto oscuro para mejor contraste */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    /* Estilos para el código dentro de las tarjetas */
    .constraint-card code, .fk-card code, .index-card code {
        background-color: rgba(0,0,0,0.05);
        padding: 2px 4px;
        border-radius: 3px;
        color: #d63384;  /* Color para que destaque */
        font-family: SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Inspector de Esquema de Base de Datos")

# Inicializar variables de sesión si no existen
if 'tables' not in st.session_state:
    st.session_state.tables = []
if 'selected_table' not in st.session_state:
    st.session_state.selected_table = None
if 'show_create_statement' not in st.session_state:
    st.session_state.show_create_statement = False

# Botón para cargar/recargar las tablas
if st.button("🔄 Cargar tablas"):
    try:
        st.session_state.tables = get_tables()
        st.success(f"✅ Se han cargado {len(st.session_state.tables)} tablas con éxito.")
    except Exception as e:
        st.error(f"❌ Error al conectar con la base de datos: {e}")

# Mostrar el selector de tablas si hay tablas disponibles
if st.session_state.tables:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_table = st.selectbox(
            "📋 Selecciona una tabla", 
            st.session_state.tables,
            index=0 if st.session_state.selected_table is None else st.session_state.tables.index(st.session_state.selected_table) if st.session_state.selected_table in st.session_state.tables else 0
        )
    
    with col2:
        st.session_state.show_create_statement = st.checkbox("Mostrar CREATE TABLE", value=st.session_state.show_create_statement)
    
    # Actualizar la tabla seleccionada en la sesión
    st.session_state.selected_table = selected_table
    
    # Mostrar la estructura de la tabla seleccionada
    if selected_table:
        try:
            table_info = get_table_full_info(selected_table)
            
            # Encabezado con información general
            st.markdown(f"## 📊 Tabla: `{selected_table}`")
            
            # Metadatos de la tabla
            with st.expander("📝 Metadatos de la tabla", expanded=True):
                meta_cols = st.columns(3)
                
                if 'metadata' in table_info and table_info['metadata']:
                    metadata = table_info['metadata']
                    
                    with meta_cols[0]:
                        st.markdown("### Propiedades básicas")
                        st.markdown(f"**Motor:** {metadata.get('ENGINE', 'N/A')}")
                        st.markdown(f"**Filas (aprox.):** {metadata.get('TABLE_ROWS', 'N/A')}")
                        st.markdown(f"**Formato:** {metadata.get('ROW_FORMAT', 'N/A')}")
                        
                    with meta_cols[1]:
                        st.markdown("### Almacenamiento")
                        st.markdown(f"**Tamaño datos:** {round(metadata.get('DATA_LENGTH', 0)/1024/1024, 2)} MB")
                        st.markdown(f"**Tamaño índices:** {round(metadata.get('INDEX_LENGTH', 0)/1024/1024, 2)} MB")
                        st.markdown(f"**Longitud media de fila:** {metadata.get('AVG_ROW_LENGTH', 'N/A')} bytes")
                        
                    with meta_cols[2]:
                        st.markdown("### Otros")
                        st.markdown(f"**Collation:** {metadata.get('TABLE_COLLATION', 'N/A')}")
                        st.markdown(f"**AUTO_INCREMENT:** {metadata.get('AUTO_INCREMENT', 'N/A')}")
                        st.markdown(f"**Creada:** {metadata.get('CREATE_TIME', 'N/A')}")
                        
                    if metadata.get('TABLE_COMMENT'):
                        st.markdown("### Descripción")
                        st.info(f"{metadata.get('TABLE_COMMENT', '')}")
            
            # Mostrar información de columnas
            if 'columns' in table_info and table_info['columns']:
                st.markdown("### 📋 Estructura de columnas")
                
                # Convertir a DataFrame para mejor visualización
                df_columns = pd.DataFrame(table_info['columns'])
                
                # Marcar las claves primarias
                if 'primary_keys' in table_info and table_info['primary_keys']:
                    df_columns['PK'] = df_columns['COLUMN_NAME'].apply(lambda x: "✅" if x in table_info['primary_keys'] else "")
                
                # Seleccionar y ordenar columnas para el DataFrame
                display_columns = ['COLUMN_NAME', 'COLUMN_TYPE', 'IS_NULLABLE', 'COLUMN_DEFAULT', 'EXTRA', 'PK']
                display_names = ['Nombre', 'Tipo', '¿Nulo?', 'Valor por defecto', 'Extra', 'PK']
                
                # Filtrar columnas que existen en el DataFrame
                available_columns = [col for col in display_columns if col in df_columns.columns]
                
                # Si hay comentarios, incluirlos
                if 'COLUMN_COMMENT' in df_columns.columns:
                    available_columns.append('COLUMN_COMMENT')
                    display_names.append('Comentario')
                
                df_display = df_columns[available_columns]
                df_display.columns = display_names[:len(available_columns)]
                
                # Mostrar el DataFrame
                st.dataframe(df_display, use_container_width=True)
            
            # Mostrar claves foráneas
            if 'foreign_keys' in table_info and table_info['foreign_keys']:
                st.markdown("### 🔗 Claves foráneas")
                
                for fk in table_info['foreign_keys']:
                    st.markdown(f"""
                    <div class="fk-card">
                        <span class="badge badge-primary">FK</span>
                        <b>{fk['CONSTRAINT_NAME']}</b>: Columna <code>{fk['COLUMN_NAME']}</code> 
                        referencia <code>{fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}</code>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Mostrar índices
            if 'indexes' in table_info and table_info['indexes']:
                st.markdown("### 📑 Índices")
                
                for idx in table_info['indexes']:
                    idx_type = "UNIQUE" if idx['NON_UNIQUE'] == 0 else "INDEX"
                    badge_class = "badge-success" if idx['NON_UNIQUE'] == 0 else "badge-secondary"
                    
                    st.markdown(f"""
                    <div class="index-card">
                        <span class="badge {badge_class}">{idx_type}</span>
                        <b>{idx['INDEX_NAME']}</b>: Columnas <code>{idx['columns_list']}</code>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Mostrar el CREATE TABLE statement si está activado
            if st.session_state.show_create_statement and 'create_script' in table_info:
                st.markdown("### 📜 CREATE TABLE")
                st.code(table_info['create_script'], language="sql")
            
        except Exception as e:
            st.error(f"❌ Error al obtener la información de la tabla: {e}")
elif st.session_state.tables == []:
    st.info("⚠️ No se encontraron tablas en la base de datos.")
else:
    st.info("👆 Haz clic en el botón para cargar las tablas de la base de datos.")
