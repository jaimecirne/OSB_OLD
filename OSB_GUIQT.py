#! /usr/bin/env python
"""
OctopusSleepBehavior GUI QT


"""
# Authors: Inácio Gomes Medeiros (inacio.medeiros@neuro.ufrn.br) and Jaime Bruno Cirne de Oliveira (jaime@neuro.ufrn.br)

from __future__ import division
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch, Circle
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from collections import Counter
from functools import reduce
import numpy as np
import sys
import os
from collections import defaultdict
import matplotlib.patches as mpatch
import scipy as sp
import time
from math import log
from matplotlib.colors import LinearSegmentedColormap

class OSBWidget(QtWidgets.QMainWindow):

    # buttons inputs
    NumButtons = ['open','save']

    states = []
    nodes_time_seconds = {}
    states_len = 0
    type_plot_standard_graph = True
    type_plot_ajd_matrix = False
    display_weight = True
    display_weight_as_porcent = False
    display_proportional_size_node = False
    display_print_size = False
    display_colorful_graph = False
    display_percent = True
    display_fancy = True

    # texts to windows titles
    text_window_title_main = 'Octopus Sleep Behavior'
    text_window_title_QFileDialog_open = 'Data file selection'
    text_window_title_QFileDialog_save = 'Save plot graph PDF'
    text_window_title_QMessageBox_error_plot = "It's not possible plot"
    text_window_title_QMessageBox_error_save = 'Error to save the PDF file'
    text_window_title_QMessageBox_OK_save = 'Confirmation'
    text_window_title_QMessageBox_error_load = 'File is not load'
    text_QMessageBox_error_load = 'You need load a CSV file on open option first. If you have done this, verify if you had chosen a valid file.'

    # texts to interfaces inputs
    text_QLabel_graph_type = 'Plot type'
    text_QRadioButton_standard = 'Graph Standard'
    text_QRadioButton_adj_matrix = 'Adjacency Matrix'
    text_QLabel_other_options = 'Other options'
    text_QCheckBox_weight = 'Display weight'
    text_QCheckBox_percentage = 'Display weight as %'
    text_QCheckBox_colorful = 'Display colorful graph'
    text_QCheckBox_proportional_size_node = 'Display node proportional size by time'
    text_QCheckBox_size_print = 'Display graph in a custom size'

    # text to MSG
    text_QMessageBox_error_open = 'You need load a CSV file on open option first. If you have done this, verify if you had chosen a valid file.'
    text_QMessageBox_error_save = 'Verify if you have write permission in this path'
    text_QMessageBox_OK_save = 'item saved successfully'

    # filter files
    text_filter_CSVFile = 'CSV Files (*.csv)'
    text_filter_PDFFile = 'PDF Files (*.pdf)'

    FONT_SIZE = 16
    NODE_SIZE = 5800
    head_length = 0.4
    head_width = 0.2
    Arrow_Style = '->'

    def __init__(self):

        super(OSBWidget, self).__init__()
        font = QFont()
        font.setPointSize(self.FONT_SIZE)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1600, 800)
        self.center()
        self.setWindowTitle(self.text_window_title_main)

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox()

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure(figsize=(40, 40))
        self.figure.tight_layout()
        self.size_inches_old = self.figure.get_size_inches()
        self.canvas = FigureCanvas(self.figure)

        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        #grid.addLayout(buttonLayout, 0, 0)
        #grid.addWidget(self.canvas, 0, 1, 40, 40)

        self.widget.layout().addWidget(self.verticalGroupBox)

        self.widget.layout().addWidget(self.scroll)

        self.canvas.draw()

        self.showMaximized()
        self.show()


    def scrolling(self, event):
        val = self.scroll.verticalScrollBar().value()
        if event.button =="down":
            self.scroll.verticalScrollBar().setValue(val+100)
        else:
            self.scroll.verticalScrollBar().setValue(val-100)

    def createVerticalGroupBox(self):

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('File')
        self.plotMenu = self.menubar.addMenu(self.text_QLabel_graph_type)


        self.impMenu = QMenu('Save as ', self)
        self.impPDFAct = QAction('Save as PDF', self) 
        self.impMenu.addAction(self.impPDFAct)

        self.impPDFAct.triggered.connect(lambda:self.save())

        self.openAct = QAction('Open Sheet', self)        

        self.openAct.triggered.connect(lambda:self.open())

        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.impMenu)

        self.verticalGroupBox = QGroupBox()

        myFont= QFont()
        myFont.setBold(True)

        layout = QHBoxLayout()

        self.verticalGroupBox.setLayout(layout)

        #labe type plot
        label_type = QLabel(self.text_QLabel_graph_type)
        label_type.setFont(myFont)
        layout.addWidget(label_type)

        #radio type plot standard
        self.gs = QRadioButton(self.text_QRadioButton_standard)
        self.gs.setChecked(True)
        self.gs.toggled.connect(lambda:self.btnstate(self.gs))
        layout.addWidget(self.gs)

        #radio type plot curved
        self.am = QRadioButton(self.text_QRadioButton_adj_matrix)
        self.am.toggled.connect(lambda:self.btnstate(self.am))
        layout.addWidget(self.am)

        layout.setSpacing(10)

#        label_type = QLabel(self.text_QLabel_other_options)

#        label_type.setFont(myFont)

#        layout.addWidget(label_type)

        self.dw = QCheckBox(self.text_QCheckBox_weight)

        self.dw.setChecked(True)

        self.dw.toggled.connect(lambda:self.checkStateWeight(self.dw))

        layout.addWidget(self.dw)

        self.dwp = QCheckBox(self.text_QCheckBox_percentage)

        self.dwp.toggled.connect(lambda:self.checkStatePercent(self.dwp))

        layout.addWidget(self.dwp)

#        self.color_graph = QCheckBox(self.text_QCheckBox_colorful)

#        self.color_graph.toggled.connect(lambda:self.checkStateColor(self.color_graph))

#        layout.addWidget(self.color_graph)

#        self.proportional_size_node = QCheckBox(self.text_QCheckBox_proportional_size_node)

#        self.proportional_size_node.toggled.connect(lambda:self.checkPSN(self.proportional_size_node))

#        layout.addWidget(self.proportional_size_node)


        validator = QDoubleValidator(0.0, 5.0, 2)

        self.arrowTypeLabel = QLabel(self)
        self.arrowTypeLabel.setText('Arror type:')
        layout.addWidget(self.arrowTypeLabel)
        self.arrowType = QComboBox()
        self.arrowType.addItems(["->", "-|>", "<-", "<->", "<|-", "<|-|>", "fancy", "simple"])
        self.arrowType.currentIndexChanged.connect(self.selectionchange)
        layout.addWidget(self.arrowType)


        self.show_p = QCheckBox('Show % ')
        self.show_p.setChecked(True)
        self.show_p.toggled.connect(lambda:self.checkShow_p(self.show_p))
        layout.addWidget(self.show_p)

        self.show_fancy = QCheckBox('Fancy Background')
        self.show_fancy.setChecked(True)
        self.show_fancy.toggled.connect(lambda:self.checkShowFancy(self.show_fancy))
        layout.addWidget(self.show_fancy)

        self.headLengthLabel = QLabel(self)
        self.headLengthLabel.setText('head length:')
        layout.addWidget(self.headLengthLabel)

        self.headLengthline = QLineEdit(self)
        self.headLengthline.setValidator(validator)
        self.headLengthline.setText(str(self.head_length))
        self.headLengthline.textChanged.connect(lambda: self.checkhl(self.headLengthline))
        layout.addWidget(self.headLengthline)

        self.headWidthLabel = QLabel(self)
        self.headWidthLabel.setText('head width:')
        layout.addWidget(self.headWidthLabel)

        self.headWidthline = QLineEdit(self)
        self.headWidthline.setValidator(validator)
        self.headWidthline.setText(str(self.head_width))
        self.headWidthline.textChanged.connect(lambda: self.checkhw(self.headWidthline))
        layout.addWidget(self.headWidthline)

        self.fontSizeLabel = QLabel(self)
        self.fontSizeLabel.setText('Font Size:')
        layout.addWidget(self.fontSizeLabel)

        self.fontSizeline = QLineEdit(self)
        self.fontSizeline.setValidator(validator)
        self.fontSizeline.setText(str(self.FONT_SIZE))
        self.fontSizeline.textChanged.connect(lambda: self.checkSF(self.fontSizeline))

        layout.addWidget(self.fontSizeline)

        self.nodeSizeLabel = QLabel(self)

        self.nodeSizeLabel.setText('Node Size:')

        layout.addWidget(self.nodeSizeLabel)

        self.nodeSizeline = QLineEdit(self)

        self.nodeSizeline.setValidator(validator)

        self.nodeSizeline.setText(str(self.NODE_SIZE))

        self.nodeSizeline.textChanged.connect(lambda: self.checkSN(self.nodeSizeline))

        layout.addWidget(self.nodeSizeline)

        self.size_print = QCheckBox(self.text_QCheckBox_size_print)

        self.size_print.toggled.connect(lambda:self.checkSP(self.size_print))

        layout.addWidget(self.size_print)

        self.heightLabel = QLabel(self)

        self.heightLabel.setText('height:(in inch)')

        layout.addWidget(self.heightLabel)

        self.heightline = QLineEdit(self)

        self.heightline.setValidator(validator)

        self.heightline.setText("10")

        self.heightline.textChanged.connect(lambda: self.checkSP(self.heightline))

        self.heightline.setDisabled(True)

        layout.addWidget(self.heightline)

        self.slheight = QSlider(Qt.Horizontal)

        self.slheight.setMinimum(5)
        
        self.slheight.setMaximum(100)
        
        self.slheight.setValue(10)
        
        self.slheight.setTickPosition(QSlider.TicksBelow)
        
        self.slheight.setTickInterval(5)

        self.slheight.valueChanged.connect(self.valuechangeheight)

        layout.addWidget(self.slheight)

        self.widthLabel = QLabel(self)
                
        self.widthLabel.setText('width (in inch):')

        layout.addWidget(self.widthLabel)

        self.widthline = QLineEdit(self)

        self.widthline.setValidator(validator)

        self.widthline.setText("10")

        self.widthline.textChanged.connect(lambda: self.checkSP(self.widthline))

        self.widthline.setDisabled(True)

        layout.addWidget(self.widthline)

        self.slwidth = QSlider(Qt.Horizontal)

        self.slwidth.setMinimum(5)

        self.slwidth.setMaximum(100)

        self.slwidth.setValue(10)

        self.slwidth.setTickPosition(QSlider.TicksBelow)

        self.slwidth.setTickInterval(5)

        self.slwidth.valueChanged.connect(self.valuechangewidth)

        layout.addWidget(self.slwidth)



    def checkPSN(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_proportional_size_node = self.proportional_size_node.isChecked()
            self.plot()

    def checkSN(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            new_node_size = self.nodeSizeline.text().strip()
            if(new_node_size != ""):
                self.NODE_SIZE = int(new_node_size)
                self.plot()

    def selectionchange(self,i):
        self.Arrow_Style = self.arrowType.currentText()
        self.plot()

    def checkhw(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            new_hw = self.headWidthline.text().strip()
            if(new_hw != ""):
                self.head_width = float(new_hw)
                self.plot()

    def checkhl(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            new_hl = self.headLengthline.text().strip()
            if(new_hl != ""):
                self.head_length = float(new_hl)
                self.plot()

    def checkSF(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            new_font_side = self.fontSizeline.text().strip()
            if(new_font_side != ""):
                self.FONT_SIZE = int(new_font_side)
                self.plot()

    def checkSP(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            new_h = self.heightline.text().strip()
            new_w = self.widthline.text().strip()
            if (new_h != "" and new_w != ""):
                if(int(new_h) > 0 and int(new_w) > 0):
                    self.display_print_size = self.size_print.isChecked()
                    if(self.display_print_size):
                        self.widthline.setDisabled(False)
                        self.heightline.setDisabled(False)
                        self.width_print = float(new_w)
                        self.height_print = float(new_h)
                    else:
                        self.widthline.setDisabled(True)
                        self.heightline.setDisabled(True)
                        self.figure.set_size_inches(self.size_inches_old)
                    self.plot()

    def checkStatePercent(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_weight_as_porcent = self.dwp.isChecked()
            self.plot()

    def checkShowFancy(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_fancy = self.show_fancy.isChecked()
            self.plot()

    def checkShow_p(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_percent = self.show_p.isChecked()
            self.plot()

    def checkStateWeight(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_weight = self.dw.isChecked()
            self.plot()

    def checkStateColor(self, g):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.display_colorful_graph = self.color_graph.isChecked()
            self.plot()

    def btnstate(self, g):
        if g.text() == self.text_QRadioButton_standard:
            self.type_plot_standard_graph = g.isChecked()
            self.type_plot_ajd_matrix = not g.isChecked()
            self.dwp.setEnabled(True)
            if (len(self.states) <= 0):
                self.showdialogErrorLoad()
            else:
                self.plot()

        if g.text() == self.text_QRadioButton_adj_matrix:
            self.type_plot_standard_graph = not g.isChecked()
            self.type_plot_ajd_matrix = g.isChecked()
            self.dwp.setDisabled(True)
            if (len(self.states) <= 0):
                self.showdialogErrorLoad()
            else:
                self.plot()

    def valuechangewidth(self):
        width = self.slwidth.value()
        self.widthline.setText(str(width))

    def valuechangeheight(self):
        height = self.slheight.value()
        self.heightline.setText(str(height))

    def submitCommand(self):
        eval('self.' + str(self.sender().objectName()) + '()')

    def showdialogMSGBox(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, self.text_window_title_QFileDialog_open, os.getenv('.'),self.text_filter_CSVFile, options=options)
        if (self.fileName != ''):
            with open(self.fileName, 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    self.states.append(row)
                self.states_len = len(self.states)
                self.plot()

    def replot  (self):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            self.plot()

    #this method mount one Directed graphs with the loaded data from CSV file
    def mountDiGraph(self):
        def rename(name):
            name_return = ''
            if name in {'Alert', 'Active'}:
                name_return = name
            elif name == 'Long SWS-like':
                name_return = f'*Long\n{name[5:]}'
            elif name == 'Short SWS-like':
                name_return = f'*Short\n{name[6:]}'
            else:
                name_return = f'*{name}'
            return name_return

        edges =[]
        self.nodes_time_seconds = {}
        G = None
        for i, s in enumerate(self.states):
                if i > 0 and i < (self.states_len -1):
                    edges.append((
                        rename(self.states[i][0]),
                        rename(self.states[i+1][0])
                    ))

        for s in self.states:
            hour = int(s[1].split(':')[0])
            minutes = int(s[1].split(':')[1])
            seconds = int(s[1].split(':')[2])

            if s[0] in self.nodes_time_seconds:
                self.nodes_time_seconds[s[0]] = self.nodes_time_seconds[s[0]] + hour*3600  + minutes*60 + seconds
            else:
                self.nodes_time_seconds[s[0]] = hour*3600  + minutes*60 + seconds

        print(self.nodes_time_seconds)

        if (self.display_weight_as_porcent and not self.type_plot_ajd_matrix):
            absolut_weight = [[x,v] for (x, y), v in Counter(edges).items()]
            nodes_weight = {}

            for aw in absolut_weight:
                if aw[0] in nodes_weight:
                    nodes_weight[aw[0]] = nodes_weight[aw[0]] + aw[1]
                else:
                    nodes_weight= {**nodes_weight, **{aw[0]:aw[1]}}

            if (self.display_weight):
                perc_values = {
                    (xa, ya): va / sum([vb for (xb, yb), vb in Counter(edges).items() if yb == ya])
                    for (xa, ya), va in Counter(edges).items()
                }

                # G = nx.DiGraph(
                #     (x, y, {'weight': str(v)+'\n'+'{:.0%}'.format((perc_values[(x, y)]))})
                #     for (x, y), v in Counter(edges).items()
                # )

                if self.display_percent:
                    G = nx.DiGraph((x, y, {'weight': ('{:.0%}'.format((perc_values[(x, y)])))}) for (x, y), v in Counter(edges).items())
                else:
                    G = nx.DiGraph((x, y, {'weight': ('{:.0%}'.format((perc_values[(x, y)])))[:-1]}) for (x, y), v in Counter(edges).items())

                # G = nx.DiGraph(
                #     (x, y, {'weight': str(v)+'\n'+'{:.0%}'.format((v/nodes_weight[x]))})
                #     for (x, y), v in Counter(edges).items()
                # )
            else:
                if self.display_percent:
                    G = nx.DiGraph((x, y, {'weight':  '{:.0%}'.format((v/nodes_weight[x]))}) for (x, y), v in Counter(edges).items())                
                else:
                    G = nx.DiGraph((x, y, {'weight':  '{:.0%}'.format((v/nodes_weight[x]))[:-1] }) for (x, y), v in Counter(edges).items())

        elif (self.display_weight and not self.type_plot_ajd_matrix):
            G = nx.DiGraph((x, y, {'weight': v}) for (x, y), v in Counter(edges).items())
            print(G.edges)
        else:
            G = nx.DiGraph((x, y, {'weight': ''}) for (x, y), v in Counter(edges).items())

        #this line list the created edges -> print(*G.edges(data=True), sep='\n')
        #this line list the created nodes -> print(*G.nodes(data=True), sep='\n')
        return G

    def plotAdjMatrix(self, G):

        print ('start')
        print(G)
        print ('end')
        adj_matrix = nx.adjacency_matrix(G)

        plt.imshow(adj_matrix.toarray())

        plt.title('Adjacency Matrix')
        plt.colorbar()

        nodes = G.nodes(data=True)

        classes = []

        [classes.append(n[0]) for n in nodes]

        for i in range(len(classes)):
            for j in range(len(classes)):
                text = plt.text(j, i, adj_matrix[i, j], ha="center", va="center", color="w")

        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        plt.tight_layout()
        #plt.ylabel('True label')
        #plt.xlabel('Predicted label')

    def plotStandardGraph(self, G):
        # G = nx.relabel_nodes(G, {
        #     'Alerta': 'Alert',
        #     'Ativo': 'Active',
        #     'Quieto': 'QOP',
        #     'AMMD': 'QHH',
        #     'AMME': 'QHH',
        #     'QMMD': 'QHH',
        #     'QMME': 'QHH',
        #     'QPC': 'SWS-like',
        #     'REM': 'REM-like',
        #     'REMD': 'One eye Movement',
        # })

        color_node_ref = {
            'Alert': '#FF8C00', # Alert
            'Active': '#FF0000', # Active
            '*QOP': '#00BFFF', # ???????
            '*QHH': '#4169E1', # ??????? 
            '*QHH': '#4169E1', # ??????? 
            '*QHH': '#4169E1', # Half and Half
            '*QHH': '#4169E1', # Open pupil
            '*SWS-like': '#87CEEB', # Closed pupil
            '*Long\nSWS-like': '#0000CD', # Long SWS-like
            '*Short\nSWS-like': '#87CEEB', # Short SWS-like
            '*REM-like': '#32CD32', # REM-like
            '*OEM': '#008000', # One eye Movement
        }

        def add_color(colors, node):
            colors.append(color_node_ref.get(node, '#0000FF'))
            return colors

        # print('------------------------------')
        # for n in G.nodes:
        #     print(n)
        # print('------------------------------')
        # pos = nx.layout.shell_layout(G)
        pos = nx.layout.circular_layout(G, scale=10) # positions for all nodes

        node_sizes = self.NODE_SIZE
        # node_colors = 'blue'
        node_colors = reduce(add_color, G.nodes, [])
        
        if(self.display_proportional_size_node):
            node_sizes = []
            for i in self.nodes_time_seconds:
                node_sizes.append(log(self.nodes_time_seconds[i], 10)*1000)

        if(self.display_colorful_graph):
            node_colors = []
            for i in self.nodes_time_seconds:
                node_colors.append(self.nodes_time_seconds[i])
            


        # print nodes
        nodes = nx.draw_networkx_nodes(
            G,
            pos,
            node_size=node_sizes,
            node_color=node_colors,
            #node_cmap=plt.get_cmap('jet'),
            cmap=plt.get_cmap('jet'),
        )
        
        # print the nodes' label
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=self.FONT_SIZE,
            font_color='w',
            font_family='sans-serif'
        )
        

        # print edges
        edges = nx.draw_networkx_edges(
            G,
            pos,
            node_size=node_sizes,
            #node_color=node_colors,
            width=2, arrowstyle= self.Arrow_Style+", head_length="+str(self.head_length)+", head_width="+str(self.head_width),
            arrowsize=10,
            edge_color='k',
            edge_cmap=plt.get_cmap('jet'),
            #cmap=plt.get_cmap('jet')
        )

        # print edges' label
        labels = nx.get_edge_attributes(G,'weight')

        #print(l[1])

        if self.display_fancy:
            nx.draw_networkx_edge_labels(
                G,
                pos,
                edge_labels=labels,
                font_size=self.FONT_SIZE,
                label_pos=0.27,
                rotate=False
            )
        else:
            nx.draw_networkx_edge_labels(
                G,
                pos,
                edge_labels=labels,
                font_size=self.FONT_SIZE,
                label_pos=0.27,
                bbox=dict(facecolor='white', edgecolor='none', pad=0), #remove the big background's label
                rotate=False
            )

        ax = plt.gca()
        ax.set_axis_off()

        #color bar
        if(self.display_colorful_graph):
            # print(node_colors)
            converted_node_colors = [int(nc/60) for nc in node_colors]
            vmin = min(converted_node_colors)
            vmax = max(converted_node_colors)
            # vmin = min(node_colors)
            # vmax = max(node_colors)
            sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin = vmin, vmax=vmax), cmap=plt.get_cmap('jet'))
            sm._A = []
            # sm.set_array(node_colors)
            sm.set_array(converted_node_colors)
            sm.set_clim(0, vmax)
            cbar = plt.colorbar(
                sm,
                boundaries=np.linspace(0, vmax, len(converted_node_colors)),
                orientation='horizontal',
            )
            cbar.ax.get_yaxis().labelpad = 20
            cbar.ax.tick_params(labelsize=self.FONT_SIZE)
            # cbar.ax.set_ylabel('Time in seconds', rotation=270)
            cbar.ax.set_xlabel('Time in minutes', rotation=0, fontsize=self.FONT_SIZE)
            #plt.colorbar(sm, boundaries=node_colors.sort())

    def showdialogErrorLoad(self):
        self.showdialogMSGBox(self.text_window_title_QMessageBox_error_load, self.text_QMessageBox_error_load)

    def plot(self):
        self.figure.clf()

        if (self.display_print_size):
            self.figure.set_size_inches( self.width_print, self.height_print)

        #create a Directed graphs with the loaded data from CSV file
        G = self.mountDiGraph()

        # this line verify if it will be a adjacenty matrix plot, if else it will be a kind of graph plot
        if (self.type_plot_ajd_matrix):
            self.plotAdjMatrix(G)   
        # chose if it will be default graph
        elif(self.type_plot_standard_graph):
            self.plotStandardGraph(G)

        self.canvas.draw_idle()

    def save(self):
        if (len(self.states) <= 0):
            self.showdialogErrorLoad()
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.filePDF, _ = QFileDialog.getSaveFileName(self,self.text_window_title_QFileDialog_save, os.getenv('HOME'), self.text_filter_PDFFile, options=options)
            if (self.filePDF != ('', '')):
                try:
                    plt.savefig(self.filePDF, format='pdf')
                    self.showdialogMSGBox(self.text_window_title_QMessageBox_OK_save, self.text_QMessageBox_OK_save)
                except  AssertionError as error:
                    self.showdialogMSGBox(self.text_window_title_QMessageBox_error_save, error)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = OSBWidget() 
    screen.show()   
    sys.exit(app.exec_())