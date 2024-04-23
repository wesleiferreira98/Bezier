from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit,QLabel,QPushButton,QMessageBox,QHBoxLayout
from PyQt5.QtCore import QPoint

from BezierCurveWidget import BezierCurveWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Curva de Bézier")
        self.setGeometry(100, 100, 800, 600)

        # Widget para exibir a curva de Bézier
        self.bezier_widget = BezierCurveWidget()

        # Campos de entrada para o número de pontos de controle
        self.num_points_label = QLabel("Número de Pontos de Controle:")
        self.num_points_input = QLineEdit()
        self.num_points_input.setText(str(self.bezier_widget.num_points))
        self.num_points_input.returnPressed.connect(self.update_num_points)

        # Botão para aplicar a interpolação da curva de Bézier
        self.interpolate_button = QPushButton("Começar Animação")
        self.interpolate_button.clicked.connect(self.pause_resume_animation)

        self.edit_check_points = QPushButton("Alterar os pontos")
        self.edit_check_points.clicked.connect(self.update_num_points)

        self.current_possition = QLabel("Posição atual do ponto verde: 0.0")

        layoutH= QHBoxLayout()
        layoutH.addWidget(self.num_points_input)
        layoutH.addWidget(self.edit_check_points)


        layoutHNumPont= QHBoxLayout()
        layoutHNumPont.addWidget(self.num_points_label)
        layoutHNumPont.addWidget(self.current_possition)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.bezier_widget)
        layout.addLayout(layoutHNumPont)
        layout.addLayout(layoutH)
        layout.addWidget(self.interpolate_button)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Desenha a curva padrão inicialmente
        self.bezier_widget.update()

        # Configurações de estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #9dcfff;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #1E90FF;
                border: none;
                color: white;
                text-align: center;
                font-size: 16px;
                padding: 10px 20px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QLineEdit {
                background-color: #aecdeb;
                border-radius: 5px;
                border: 2px solid #1E90FF; /* Cor da borda */
                padding: 5px 10px;
                margin: 2px 2px;
            }
             QProgressBar {
                border: none;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QProgressBar::chunk {
                background-color: #1E90FF; /* Cor da barra de progresso */
                width: 10px; /* Largura da barra de progresso */
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1C86EE;
            }
        """)

        # Variável de controle para pausar/resumir a animação
        self.animation_paused = True

        # Conecta o sinal timeout do QTimer à função para atualizar a posição do ponto verde
        self.bezier_widget.timer.timeout.connect(self.update_position_label)

    def update_num_points(self):
        # Atualiza o número de pontos de controle com base no valor inserido pelo usuário
        try:
            num_points = int(self.num_points_input.text())
            if num_points >= 2:
                self.bezier_widget.num_points = num_points
                self.bezier_widget.points = [QPoint(50 + i * 100, 200) for i in range(num_points)]
                self.bezier_widget.update()
            else:
                QMessageBox.warning(self,"Atenção","O número de pontos de controle deve ser pelo menos 2.")
                raise ValueError("O número de pontos de controle deve ser pelo menos 2.")
        except ValueError as e:
            print(e)
            QMessageBox.warning(self,"Atenção","Somente números são aceitos")
            self.num_points_input.setText(str(self.bezier_widget.num_points))

    def interpolate_curve(self):
        # Interpola a curva de Bézier com os pontos de controle fornecidos pelo usuário
        self.bezier_widget.update()
    
    def pause_resume_animation(self):
        # Pausa ou resume a animação ao clicar no botão
        if self.animation_paused:
            self.bezier_widget.timer.start()
            self.interpolate_button.setText("Pausar")
        else:
            self.bezier_widget.timer.stop()
            self.interpolate_button.setText("Resumir")
        self.animation_paused = not self.animation_paused

    def update_position_label(self):
        # Atualiza o texto do QLabel com a posição atual do ponto verde
        numP = "Posição atual do ponto verde: " + str(self.bezier_widget.current_point_index)
        self.current_possition.setText(numP)
