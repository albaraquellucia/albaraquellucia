import streamlit as st


import streamlit as st
import requests
import json

# Función para generar código SQL y explicación usando Gemini
def generate_sql_and_explanation(context, question, api_key):
    """
    Genera código SQL para BigQuery y su explicación usando la API de Gemini.

    Args:
        context: Contexto sobre la base de datos (esquema, tablas, etc.).
        question: Pregunta en lenguaje natural.
        api_key: Clave de API de Google Generative AI.

    Returns:
        Un diccionario con el código SQL y la explicación, o None si hay un error.
    """
    try:
        # Construir el prompt para Gemini
        prompt = f"""
        Contexto de la Base de Datos:
        {context}

        Pregunta:
        {question}

        Instrucciones:
        1. Genera el código SQL para BigQuery que responda a la pregunta.
        2. Luego, explica el código SQL generado en lenguaje natural, paso a paso.
        3. Separa el codigo sql de la explicacion con la palabra reservada SEPARADORSQL
        """

        # Construir el payload para la API de Gemini
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Llamar a la API de Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

        # Procesar la respuesta
        response_json = response.json()

        #Extraemos el texto de la respuesta
        response_text = response_json['candidates'][0]['content']['parts'][0]['text']

        #buscamos el separador
        separator = "SEPARADORSQL"

        #extraemos el codigo sql y la explicacion
        sql_code, explanation = response_text.split(separator)

        # Formatear la respuesta
        return {
            "sql_code": sql_code.strip(),
            "explanation": explanation.strip()
        }

    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión a la API: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar la respuesta JSON: {e}")
        return None
    except KeyError as e:
        st.error(f"Error al acceder a la respuesta JSON: {e}. Verifica la estructura de la respuesta de la API. Clave faltante: {e}")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None


# Interfaz de Streamlit
st.title("Hola, soy tu chat personalizado de SQL, ¿en qué puedo ayudarte? :3")

# Área de entrada para la clave de API
api_key = st.text_input("Clave API de Google Generative AI:", type="password")  # type="password" oculta la clave

# Área de entrada para el contexto de la base de datos
context = st.text_area("Contexto de la Base de Datos (Esquema, Tablas, etc.):", height=200)

# Área de entrada para la pregunta en lenguaje natural
question = st.text_input("Pregunta en Lenguaje Natural:")

# Botón para generar el código SQL
if st.button("Generar SQL"):
    if not api_key:
        st.warning("Por favor, introduce tu Clave API.")
    elif not context:
        st.warning("Por favor, proporciona el contexto de la base de datos.")
    elif not question:
        st.warning("Por favor, introduce una pregunta.")
    else:
        # Generar el código SQL y la explicación
        result = generate_sql_and_explanation(context, question, api_key)

        if result:
            # Mostrar el código SQL
            st.subheader("Código SQL Generado:")
            st.code(result["sql_code"], language="sql")

            # Mostrar la explicación
            st.subheader("Explicación:")
            st.write(result["explanation"])
        else:
            st.error("No se pudo generar el código SQL. Revisa los errores.")

# Info adicional (Opcional)
st.sidebar.header("Información Adicional")
st.sidebar.markdown(
    """
    Esta aplicación utiliza la API de Google Generative AI (Gemini) para generar código SQL 
    para BigQuery a partir de una pregunta en lenguaje natural y el contexto de la base de datos.
    """
)
st.sidebar.markdown(
    """
    **Importante:**
    *   Asegúrate de tener una cuenta de Google Cloud Platform (GCP) y la API de Gemini habilitada.
    *   La clave API debe almacenarse de forma segura (por ejemplo, usando `st.secrets`).
    *   El rendimiento de la API depende de la calidad del contexto y la claridad de la pregunta.
    """
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #ADD8E6;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Configuración de la sesión (para el ejemplo del historial del chat)
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Estilos CSS personalizados
st.markdown("""
<style>
.chat-message {
    background-color: #f0f2f6;
    padding: 0.5em;
    border-radius: 0.5em;
    margin-bottom: 0.5em;
}

.user-message {
    background-color: #e2f0ff;
    text-align: right;
}

.bot-message {
    background-color: #f0f2ff;
    text-align: left;
}

.thank-you-box {
    background-color: #e6ffe6;  /* Color de fondo del cuadro de agradecimiento */
    border: 1px solid #b3ffb3;  /* Borde del cuadro */
    padding: 1em;
    border-radius: 0.5em;
    margin-top: 1em;
    text-align: center; /* Centrar el texto */
    font-weight: bold; /* Poner el texto en negrita */
    font-size: 1.5em; /* Aumentar el tamaño del texto */
}
</style>
""", unsafe_allow_html=True)





# Cuadro de agradecimiento
st.markdown('<div class="thank-you-box">¡Gracias por usar el chat!</div>', unsafe_allow_html=True)