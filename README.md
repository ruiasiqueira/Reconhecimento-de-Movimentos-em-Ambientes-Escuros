#Reconhecimento de Gestos em ambientes escuros, para acionar alertas ou sinais.

#Problema a ser solucionado:

Em ambientes escuros, câmeras comuns não captam formas ou silhuetas, fazendo com que movimentos passem despercebidos. 
Sem luz suficiente, as câmeras não distinguem mudanças de cena e o cenário escuro, gerando “falsos negativos” 
de invasão. Isso significa que alguém pode se mover livremente sem acionar alarmes ou ser gravado, pois o software de 
vigilância não enxerga o contraste necessário. Mesmo câmeras com bateria continuam “cegas” no escuro absoluto. 
Por isso, soluções que clareiam a imagem ou usam sensores que não dependem de luz são essenciais para detectar 
movimentos e manter a segurança durante apagões.

######################################


Este script em Python processa um vídeo gravado em ambiente escuro (`IMG_7227.MOV`),
clareia cada frame, compara com o frame anterior para detectar movimento e desenha:

* Retângulos verdes ao redor das áreas em movimento
* Pontos amarelos em cada pixel do contorno
* Mensagem de alerta em vermelho **“ALERTA : MOVIMENTO DETECTADO”** sobre o vídeo

Além disso, imprime no console tanto o JSON indicando se houve movimento:

json
{"movimento": 1}  // movimento detectado
{"movimento": 0}  // sem movimento


Mensagem de alerta que aparece na tela:

ALERTA : MOVIMENTO DETECTADO


#Bibliotecas Necessárias

opencv-python: Captura e processamento de vídeo/imagens
numpy: Operações matriciais

#Como instalar

pip install opencv-python numpy

#Como usar

1. Coloque "main.py" e "IMG_7227.MOV" na mesma pasta.
2. Abra o terminal nessa pasta e execute:
   "python main.py"
   
3. A janela "Sensor de Movimento no Escuro"
 abrirá mostrando o vídeo com marcas de movimento e, se houver detecção, 
 exibirá a mensagem de alerta em vermelho sobre o vídeo.

#Como Parar
Na janela de exibição, pressione a tecla "ESC".
Alternativamente, feche o terminal onde o script está rodando.

#Funcionalidades em Tópicos

1. "Leitura e redimensionamento do vídeo"

   * Abre `IMG_7227.MOV` e redimensiona para 500×500 pixels.

2. "Pré-processamento para “clarear” frames escuros"

   *Ajusta brilho/contraste via
     python
     cv2.convertScaleAbs(frame, alpha=1.0, beta=150)
     
    *Converte para HSV e equaliza o canal V (valor) para reforçar contraste.

3. "Conversão para escala de cinza + blur"

   *Transforma o frame em tons de cinza (`cv2.cvtColor(..., cv2.COLOR_BGR2GRAY)`).
   *Aplica desfoque gaussiano (7×7) para reduzir ruídos.

4. "Frame differencing"

   *Calcula `absdiff(prev_gray, gray_blur)` para identificar mudanças entre frames consecutivos.
   *Aplica `threshold(25)` e dilatação para isolar regiões de movimento.

5. "Detecção de contornos"

   * Encontra contornos binários com `cv2.findContours` e filtra por área ≥ 1000 pixels.
   * Desenha retângulos verdes (`cv2.rectangle`) ao redor de cada contorno relevante.
   * Desenha pontos amarelos (`cv2.circle`) em todos os pixels do contorno.

6. "Emissão de alerta"

   * Se qualquer contorno grande for detectado, sobrepõe a mensagem 
   "ALERTA : MOVIMENTO DETECTADO" em vermelho no topo do vídeo e imprime no console:
     "ALERTA : MOVIMENTO DETECTADO"
     
   * Ainda no console, imprime o JSON:
    {"movimento": 1}

   * Se não há movimento significativo, apenas imprime:
     {"movimento": 0}


7. **Loop até ESC**

   * Atualiza "prev_gray" para o próximo ciclo e continua processando até o usuário pressionar **ESC**.

#Estrutura dos Arquivos

GS-IOT/
├── main.py           # Código
└── IMG_7227.MOV      # Vídeo em ambiente escuro

#Considerações Finais

Ajuste **BRIGHT\_BETA** (brilho) para 120, 180 ou 200, caso o vídeo esteja muito ou pouco escuro.
Modifique **MIN\_CONTOUR\_AREA** para calibrar sensibilidade a ruídos ou movimentos pequenos.

Se o OpenCV não abrir ".MOV", converta para ".mp4":
ffmpeg -i IMG_7227.MOV -c:v libx264 IMG_7227.mp4
Depois, altere em "main.py":
video_path = "IMG_7227.mp4"

A janela exibirá tanto a detecção visual (retângulos, pontos e mensagem de alerta) 
quanto o console exibirá o JSON e a string de alerta correspondente.


Autores:
Rui Amorim Siqueira - RM98436
Luan Silveira Macea- RM98290
Davi Passanha de Sousa Guerra - RM551605



