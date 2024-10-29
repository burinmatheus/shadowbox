
from shadowbox import ShadowBox

source_code = b"""import pandas as pd
import plotly.express as px

df = pd.read_csv('LogCompleto.csv')

log_counts = df.groupby('Cliente', as_index=False)['Quantidade de Logs'].sum()

fig = px.bar(log_counts, x='Cliente', y='Quantidade de Logs', title='Quantidade de Logs por Cliente')

fig.write_html('/app/grafico_interativo.html')
"""

archive_bits = ShadowBox('localhost', 2375).run(
    image_name='registry.tecnicon.com.br/python_sandbox', 
    source_code=source_code,
    files=['./LogCompleto.csv'],
    output_file_name='grafico_interativo.html',
    mem_limit='512m'
)

with open('grafico_interativo.html', 'wb') as f:
    f.write(archive_bits)