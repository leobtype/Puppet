#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from MainWidget import Ui_MainWidget
from ConfigWidget import Ui_ConfigWidget
import sys, random
import os, json
import pyaudio, wave
import numpy
from pygame import mixer, error

class MainWidget(QWidget, Ui_MainWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        # タイトルバーを非表示にする。常に最前面に表示する
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # ウィンドウ背景を透過する
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 座標設定
        if config.config.has_key('main_x') and config.config.has_key('main_y'):
            pos_x = config.config['main_x']
            pos_y = config.config['main_y']
            self.setGeometry(pos_x, pos_y, self.width(), self.height())
        # dataフォルダ検索
        self.data = []
        self.mp3media  = []
        if getattr(sys, 'frozen', False):
            if os.name == 'nt':
                datadir = os.path.join(os.environ['APPDATA'],'Puppet','data')
            else:
                datadir = os.path.join(os.environ['HOME'],'Library','Application Support','Puppet','data')
        else:
            datadir = 'data'
        if  os.path.isdir(datadir)==False:
            '''
            dataフォルダがない場合の警告
            freezeしている場合は起動時にdataフォルダを作成する
            '''
            print('Data folder is not exists.')
        for i in range(0,10):
            for d in os.listdir(datadir):
                if os.path.isdir(os.path.join(datadir,d)):
                    if d[0:1]==str(i):
                        if os.name=='nt':
                            self.data.append(d.decode('cp932'))
                        else:
                            self.data.append(d)
                        # mp3読み込み
                        for f in os.listdir(os.path.join(datadir,d)):
                            if f[-4:] == '.mp3':
                                mp3file = os.path.join(datadir,d,f)
                                self.mp3media.append(mp3file)
                                break
                        break
            if len(self.data) < i + 1:
                self.data.append('')
            if len(self.mp3media) < i + 1:
                self.mp3media.append(None)
        # 画像設定
        self.setPixmaps()
        # まばたき
        self.EYES_OPEN = True
        self.MOUSE_OPEN = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(config.config['blink_duration'])
        # 画像のリサイズ
        self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
        self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
        self.resize(self.width, self.height)
        self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        # ショートカットキー
        self.alt_1 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_1),self)
        self.alt_2 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_2),self)
        self.alt_3 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_3),self)
        self.alt_4 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_4),self)
        self.alt_5 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_5),self)
        self.alt_6 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_6),self)
        self.alt_7 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_7),self)
        self.alt_8 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_8),self)
        self.alt_9 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_9),self)
        self.alt_0 = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_0),self)
        self.alt_1.activated.connect(self.alt_1_pushed)
        self.alt_2.activated.connect(self.alt_2_pushed)
        self.alt_3.activated.connect(self.alt_3_pushed)
        self.alt_4.activated.connect(self.alt_4_pushed)
        self.alt_5.activated.connect(self.alt_5_pushed)
        self.alt_6.activated.connect(self.alt_6_pushed)
        self.alt_7.activated.connect(self.alt_7_pushed)
        self.alt_8.activated.connect(self.alt_8_pushed)
        self.alt_9.activated.connect(self.alt_9_pushed)
        self.alt_0.activated.connect(self.alt_0_pushed)

    def alt_1_pushed(self):
        if self.data[1]!='':
            if mixer.get_init()!=None:
                if self.mp3media[1]!=None:
                    mixer.music.load(self.mp3media[1])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[1]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_2_pushed(self):
        if self.data[2]!='':
            if mixer.get_init()!=None:
                if self.mp3media[2]!=None:
                    mixer.music.load(self.mp3media[2])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[2]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_3_pushed(self):
        if self.data[3]!='':
            if mixer.get_init()!=None:
                if self.mp3media[3]!=None:
                    mixer.music.load(self.mp3media[3])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[3]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_4_pushed(self):
        if self.data[4]!='':
            if mixer.get_init()!=None:
                if self.mp3media[4]!=None:
                    mixer.music.load(self.mp3media[4])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[4]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_5_pushed(self):
        if self.data[5]!='':
            if mixer.get_init()!=None:
                if self.mp3media[5]!=None:
                    mixer.music.load(self.mp3media[5])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[5]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_6_pushed(self):
        if self.data[6]!='':
            if mixer.get_init()!=None:
                if self.mp3media[6]!=None:
                    mixer.music.load(self.mp3media[6])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[6]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_7_pushed(self):
        if self.data[7]!='':
            if mixer.get_init()!=None:
                if self.mp3media[7]!=None:
                    mixer.music.load(self.mp3media[7])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[7]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_8_pushed(self):
        if self.data[8]!='':
            if mixer.get_init()!=None:
                if self.mp3media[8]!=None:
                    mixer.music.load(self.mp3media[8])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[8]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_9_pushed(self):
        if self.data[9]!='':
            if mixer.get_init()!=None:
                if self.mp3media[9]!=None:
                    mixer.music.load(self.mp3media[9])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[9]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def alt_0_pushed(self):
        if self.data[0]!='':
            if mixer.get_init()!=None:
                if self.mp3media[0]!=None:
                    mixer.music.load(self.mp3media[0])
                    mixer.music.set_volume(config.config['mp3_volume'] / 100.0)
                    mixer.music.play()
            config.config['mascot'] = self.data[0]
            self.setPixmaps()
            self.width = int(self.pixmaps[0].width() * config.config['picture_scale'])
            self.height = int(self.pixmaps[0].height() * config.config['picture_scale'])
            self.resize(self.width, self.height)
            self.label.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
            config.write()

    def setPixmaps(self):
        if getattr(sys, 'frozen', False):
            if os.name == 'nt':
                datadir = os.path.join(os.environ['APPDATA'],'Puppet','data')
                datadir = datadir.decode('cp932')
            else:
                datadir = os.path.join(os.environ['HOME'],'Library','Application Support','Puppet','data')
        else:
            datadir = 'data'
        self.pixmaps = []
        mascot = config.config['mascot']
        if os.path.isdir(os.path.join(datadir,mascot))==False:
            mascot = '0_default'
        if os.path.isdir(os.path.join(datadir,mascot)):
            for f in os.listdir(os.path.join(datadir,mascot)):
                if os.path.isfile(os.path.join(datadir,mascot,f)):
                    if f[-4:] in ['.png', '.jpg', '.gif']:
                        self.pixmaps.append(QtGui.QPixmap(os.path.join(datadir,mascot,f)))
                        if len(self.pixmaps) >= 4:
                            break
        if len(self.pixmaps)==0:
            # 画像がない
            if getattr(sys, 'frozen', False):
                mascot = '0_default'
                datadir = os.path.join(sys._MEIPASS,'data')
                for f in os.listdir(os.path.join(datadir,mascot)):
                    if os.path.isfile(os.path.join(datadir,mascot,f)):
                        if f[-4:] in ['.png', '.jpg', '.gif']:
                            self.pixmaps.append(QtGui.QPixmap(os.path.join(datadir,mascot,f)))
                            if len(self.pixmaps) >= 4:
                                break
            else:
                print('No pictures in data folder.')
        if len(self.pixmaps)==1:
            self.pixmaps.append(self.pixmaps[0])
            self.pixmaps.append(self.pixmaps[0])
            self.pixmaps.append(self.pixmaps[0])
        if len(self.pixmaps)==2:
            self.pixmaps.append(self.pixmaps[0])
            self.pixmaps.append(self.pixmaps[1])
        if len(self.pixmaps)==3:
            self.pixmaps.pop()
            self.pixmaps.append(self.pixmaps[0])
            self.pixmaps.append(self.pixmaps[1])
        if len(self.pixmaps)==4:
            # perfect!
            pass

    def update(self):
        if self.judgeSound() == False:
            self.toggleEyes()
            self.MOUSE_OPEN = False
        else:
            self.toggleEyes()
            self.toggleMouse()

        if self.MOUSE_OPEN == False and self.EYES_OPEN == True:
            self.label.setPixmap(self.pixmaps[0])
        if self.MOUSE_OPEN == False and self.EYES_OPEN == False:
            self.label.setPixmap(self.pixmaps[1])
        if self.MOUSE_OPEN == True and self.EYES_OPEN == True:
            self.label.setPixmap(self.pixmaps[2])
        if self.MOUSE_OPEN == True and self.EYES_OPEN == False:
            self.label.setPixmap(self.pixmaps[3])

    def toggleEyes(self):
        if self.EYES_OPEN == True:
            if random.random() < config.config['blink_frequency']:
                self.EYES_OPEN = False
        else:
            self.EYES_OPEN = True

    def toggleMouse(self):
        if self.MOUSE_OPEN == True:
            self.MOUSE_OPEN = False
        else:
            self.MOUSE_OPEN = True

    def mousePressEvent(self, event):
        self.timer.stop()
        # マウスクリック時のローカル座標を取得しておく。mouseMoveEventで使う
        self.clickedPosx = event.localPos().x()
        self.clickedPosy = event.localPos().y()
        QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        # マウスをクリックして動かしたときにウィジェットを動かす
        # ローカル座標が(0, 0)になってしまうので、mousePressEventで取得した
        # ローカル座標を使って補正する
        self.move(event.screenPos().x() - self.clickedPosx,
            event.screenPos().y() - self.clickedPosy)
        QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.timer.start(config.config['blink_duration'])
        QWidget.mouseMoveEvent(self, event)

    def contextMenuEvent(self, event):
        self.timer.stop()
        menu = QtWidgets.QMenu(self)
        configAction = menu.addAction('設定をひらく')
        quitAction = menu.addAction('マスコットをしまう')
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == configAction:
            self.config_widget = ConfigWidget()
            self.config_widget.show()
        if action == quitAction:
            main_widget.close()
        self.timer.start(config.config['blink_duration'])
        QWidget.contextMenuEvent(self, event)

    def closeEvent(self, event):
        config.config['main_x'] = self.geometry().x()
        config.config['main_y'] = self.geometry().y()
        config.write()
        QWidget.closeEvent(self, event)

    def judgeSound(self):
        if config.config['audio_device']!=None:
            self.audio_buffer = stream.read(config.config['audio_chunk'], exception_on_overflow=False)
            data = numpy.frombuffer(self.audio_buffer, dtype='int16')
            volume_max = max(abs(data))
            volume_threshold = int(32768 * config.config['audio_threshold'])
            if volume_max > volume_threshold:
                return True
            else:
                return False
        else:
            return False

class ConfigWidget(QWidget, Ui_ConfigWidget):

    def __init__(self, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.setupUi(self)
        # 常に最前面に表示する
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # 座標設定
        if config.config.has_key('config_x') and config.config.has_key('config_y'):
            pos_x = config.config['config_x']
            pos_y = config.config['config_y']
            self.setGeometry(pos_x, pos_y, self.width(), self.height())
        # サウンドデバイスリスト
        self.audio_input_index = []
        if config.config['audio_device']!=None:
            for i in range(int(audio.get_device_count())):
                if audio.get_device_info_by_index(i)['maxInputChannels'] > 0:
                    description = audio.get_device_info_by_index(i)['name']
                    self.comboBox.addItem(description)
                    self.audio_input_index.append(audio.get_device_info_by_index(i)['index'])
        else:
            self.audio_input_index.append('No Input Device')
        # 設定値読み込み
        if config.config['audio_device']!=None:
            self.comboBox.setCurrentIndex(self.audio_input_index.index(config.config['audio_device']))
        else:
            self.comboBox.setCurrentIndex(0)
        self.horizontalSlider.setValue(config.config['audio_threshold'] * 100)
        self.horizontalSlider_2.setValue(config.config['blink_duration'])
        self.horizontalSlider_3.setValue(config.config['blink_frequency'] * 100)
        self.horizontalSlider_4.setValue(config.config['picture_scale'] * 100)
        self.horizontalSlider_5.setValue(config.config['mp3_volume'])
        self.spinBox.setValue(config.config['picture_scale'] * 100)
        # 設定値反映
        self.comboBox.currentIndexChanged.connect(self.deviceChanged)
        self.horizontalSlider.valueChanged.connect(self.thresholdChanged)
        self.horizontalSlider_2.valueChanged.connect(self.speedChanged)
        self.horizontalSlider_3.valueChanged.connect(self.frequencyChanged)
        self.horizontalSlider_4.valueChanged.connect(self.scaleSliderChanged)
        self.horizontalSlider_5.valueChanged.connect(self.mp3volumeChanged)
        self.spinBox.valueChanged.connect(self.scaleSpinBoxChanged)
        # ボリューム表示
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateVolume)
        self.timer.start(100)
        # ボタン
        self.buttonBox.accepted.connect(self.buttonOK)
        self.buttonBox.rejected.connect(self.buttonCancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(self.buttonRestoreDefaults)

    def buttonOK(self):
        config.write()
        self.timer.stop()
        self.close()

    def buttonCancel(self):
        config.read()
        # 画像表示リサイズ
        main_widget.width = int(main_widget.pixmaps[0].width() * config.config['picture_scale'])
        main_widget.height = int(main_widget.pixmaps[0].height() * config.config['picture_scale'])
        main_widget.resize(main_widget.width, main_widget.height)
        main_widget.label.setGeometry(QtCore.QRect(0, 0, main_widget.width, main_widget.height))
        self.timer.stop()
        self.close()

    def buttonRestoreDefaults(self):
        global stream
        if config.config['audio_device']!=None:
            stream.stop_stream()
            stream.close()
        config.new()
        if config.config['audio_device']!=None:
            stream = audio.open(format=config.config['audio_format'],
                            channels=config.config['audio_channels'],
                            rate=config.config['audio_sampling_rate'],
                            input=True,
                            input_device_index=config.config['audio_device'],
                            frames_per_buffer=config.config['audio_chunk'])
        # 画像表示リサイズ
        width = int(main_widget.pixmaps[0].width() * config.config['picture_scale'])
        height = int(main_widget.pixmaps[0].height() * config.config['picture_scale'])
        main_widget.resize(width, height)
        main_widget.label.setGeometry(QtCore.QRect(0, 0, width, height))
        self.reload()

    def reload(self):
        if config.config['audio_device']!=None:
            self.comboBox.setCurrentIndex(self.audio_input_index.index(config.config['audio_device']))
        else:
            self.comboBox.setCurrentIndex(0)
        self.horizontalSlider.setValue(config.config['audio_threshold'] * 100)
        self.horizontalSlider_2.setValue(config.config['blink_duration'])
        self.horizontalSlider_3.setValue(config.config['blink_frequency'] * 100)
        self.horizontalSlider_4.setValue(config.config['picture_scale'] * 100)
        self.spinBox.setValue(config.config['picture_scale'] * 100)

    def closeEvent(self, event):
        self.timer.stop()
        config.config['config_x'] = self.geometry().x()
        config.config['config_y'] = self.geometry().y()
        config.write()
        QWidget.closeEvent(self, event)

    def updateVolume(self):
        if config.config['audio_device']!=None:
            data = numpy.frombuffer(main_widget.audio_buffer, dtype='int16')
            volume = int(max(abs(data)) * 100 / 32768.0)
            self.progressBar.setValue(volume)
        else:
            pass

    def deviceChanged(self):
        config.config['audio_device'] = self.audio_input_index[self.comboBox.currentIndex()]
        info = audio.get_device_info_by_index(self.audio_input_index[self.comboBox.currentIndex()])
        # サンプリングレート
        standard_sample_rates = [8000.0, 9600.0, 11025.0, 12000.0,
                                16000.0, 22050.0, 24000.0, 32000.0,
                                44100.0, 48000.0, 88200.0, 96000.0,
                                192000.0]
        for f in standard_sample_rates:
            try:
                if audio.is_format_supported(
                    f,
                    input_device = config.config['audio_device'],
                    input_channels = config.config['audio_channels'],
                    input_format = config.config['audio_format']):
                    config.config['audio_sampling_rate'] = int(f)
                    break
            except ValueError:
                pass
        config.config['audio_chunk'] = int(config.config['audio_sampling_rate'] * config.config['blink_duration'] / 1000)
        global stream
        if config.config['audio_device']!=None:
            stream.stop_stream()
            stream.close()
            stream = audio.open(format=config.config['audio_format'],
                            channels=config.config['audio_channels'],
                            rate=config.config['audio_sampling_rate'],
                            input=True,
                            input_device_index=config.config['audio_device'],
                            frames_per_buffer=config.config['audio_chunk'])

    def thresholdChanged(self):
        config.config['audio_threshold'] = self.horizontalSlider.value() / 100.0

    def speedChanged(self):
        config.config['blink_duration'] = self.horizontalSlider_2.value()
        main_widget.timer.stop()
        main_widget.timer.start(config.config['blink_duration'])

    def frequencyChanged(self):
        config.config['blink_frequency'] = self.horizontalSlider_3.value() / 100.0

    def scaleSliderChanged(self):
        self.spinBox.setValue(self.horizontalSlider_4.value())
        config.config['picture_scale'] = self.horizontalSlider_4.value() / 100.0
        # 画像表示リサイズ
        width = int(main_widget.pixmaps[0].width() * config.config['picture_scale'])
        height = int(main_widget.pixmaps[0].height() * config.config['picture_scale'])
        main_widget.resize(width, height)
        main_widget.label.setGeometry(QtCore.QRect(0, 0, width, height))

    def scaleSpinBoxChanged(self):
        self.horizontalSlider_4.setValue(self.spinBox.value())
        config.config['picture_scale'] = self.spinBox.value() / 100.0
        # 画像表示リサイズ
        width = int(main_widget.pixmaps[0].width() * config.config['picture_scale'])
        height = int(main_widget.pixmaps[0].height() * config.config['picture_scale'])
        main_widget.resize(width, height)
        main_widget.label.setGeometry(QtCore.QRect(0, 0, width, height))

    def mp3volumeChanged(self):
        config.config['mp3_volume'] = self.horizontalSlider_5.value()
        if mixer.get_init()!=None:
            mixer.music.set_volume(config.config['mp3_volume'])

class Config():
    if getattr(sys, 'frozen', False):
        if os.name == 'nt':
            JSON = os.path.join(os.environ['APPDATA'],'Puppet','config.json')
        else:
            JSON = os.path.join(os.environ['HOME'],'Library','Application Support','Puppet','config.json')
    else:
        JSON = 'config.json'

    def __init__(self):
        self.read()

    def read(self):
        # JSONを読み込む。なかったら新しくつくる
        # JSONの読み込みでエラーになったら破棄して新しくつくる
        if os.path.isfile(self.JSON) == True:
            try:
                with open(self.JSON, 'r') as f:
                    self.config = json.loads(f.read())
            except ValueError:
                self.new()
        else:
            self.new()

    def write(self):
        with open(self.JSON, 'w') as f:
            f.write(json.dumps(self.config, sort_keys=True, indent=4))

    def new(self):
        self.config = {}
        self.config['mascot'] = '0_default'
        self.config['blink_duration'] = 200    # タイマー間隔(ms)。まばたきの長さ
        self.config['blink_frequency'] = 0.1    # まばたき頻度
        self.config['picture_scale'] = 0.5      # 画像の拡大率
        # オーディオデバイス
        self.config['audio_device'] = None
        for i in range(0,16):
            try:
                info = audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    self.config['audio_device'] = i
                    break
            except IOError:
                pass
        if self.config['audio_device']!=None:
            self.config['audio_format'] = pyaudio.paInt16 # オーディオフォーマット
            self.config['audio_channels'] = 1             # オーディオチャネル
            # サンプリングレート
            standard_sample_rates = [8000.0, 9600.0, 11025.0, 12000.0,
                                    16000.0, 22050.0, 24000.0, 32000.0,
                                    44100.0, 48000.0, 88200.0, 96000.0,
                                    192000.0]
            for f in standard_sample_rates:
                try:
                    if audio.is_format_supported(
                        f,
                        input_device = self.config['audio_device'],
                        input_channels = self.config['audio_channels'],
                        input_format = self.config['audio_format']):
                        self.config['audio_sampling_rate'] = int(f)
                        break
                except ValueError:
                    pass
            self.config['audio_chunk'] = int(self.config['audio_sampling_rate'] * self.config['blink_duration'] / 1000)
        self.config['audio_threshold'] = 0.1          # マイク感度。0.0:敏感 - 1.0:鈍感
        self.config['mp3_volume'] = 20


if __name__ == '__main__':
    # make directory if not exists
    if getattr(sys, 'frozen', False):
        if os.name == 'nt':
            datadir = os.path.join(os.environ['APPDATA'],'Puppet','data')
            if os.path.exists(datadir)==False:
                os.makedirs(datadir)
        else:
            datadir = os.path.join(os.environ['HOME'],'Library','Application Support','Puppet','data')
            if os.path.exists(datadir)==False:
                os.makedirs(datadir)
    audio = pyaudio.PyAudio()
    config = Config()
    if config.config['audio_device']!=None:
        stream = audio.open(format=config.config['audio_format'],
                        channels=config.config['audio_channels'],
                        rate=config.config['audio_sampling_rate'],
                        input=True,
                        input_device_index=config.config['audio_device'],
                        frames_per_buffer=config.config['audio_chunk'])
    try:
        mixer.init()
    except error:
        pass
    # application and widgets
    app = QApplication(sys.argv)
    main_widget = MainWidget()

    if getattr(sys, 'frozen', False):
        window_icon = os.path.join(sys._MEIPASS, 'Puppet.ico')
    else:
        if os.name == 'nt':
            window_icon='Puppet.ico'
        else:
            pass
    if os.name == 'nt':
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(window_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        app.setWindowIcon(icon)
    else:
        pass

    main_widget.show()
    sys.exit(app.exec_())
