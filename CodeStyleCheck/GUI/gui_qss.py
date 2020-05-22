#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/5/21 0:35
# @Author : yachao_lin
# @File : gui_qss.py

qss = '''QToolTip
{
    background-color: black;
    color: white;
    padding: 0.5ex;
}

QWidget
{
    color: #31363B;
    background-color: #EFF0F1;
    selection-background-color:#33A4DF;
    selection-color: #31363B;
    background-clip: border;
    border-image: none;
    border: 0px transparent black;
    outline: 0;
}

QWidget:item:hover
{
    background-color: #33A4DF;
    color: #31363B;
}

QWidget:item:selected
{
    background-color: #33A4DF;
}

QMenuBar
{
    background-color: #EFF0F1;
    color: #31363B;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 0.1ex solid #BAB9B8;
}

QMenuBar::item:pressed
{
    border: 0.1ex solid #BAB9B8;
    background-color: #33A4DF;
    color: #31363B;
    margin-bottom: -0.1ex;
    padding-bottom: 0.1ex;
}

QMenu
{
    border: 0.1ex solid #BAB9B8;
    color: #31363B;
    margin: 0.2ex;
}

QMenu::icon
{
    margin: 0.5ex;
}

QMenu::item
{
    padding: 0.5ex 3ex 0.5ex 3ex;
    margin-left: 0.5ex;
    border: 0.1ex solid transparent; /* reserve space for selection border */
}

QMenu::item:selected
{
    color: #31363B;
}

QMenu::separator
{
    height: 0.2ex;
    background: lightblue;
    margin-left: 1ex;
    margin-right: 0.5ex;
}

/* non-exclusive indicator = check box style indicator
   (see QActionGroup::setExclusive) */
QMenu::indicator:non-exclusive:unchecked
{
    border-image: url(:/light/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:unchecked:selected
{
    border-image: url(:/light/checkbox_unchecked_disabled.svg);
}

QMenu::indicator:non-exclusive:checked
{
    border-image: url(:/light/checkbox_checked.svg);
}

QMenu::indicator:non-exclusive:checked:selected
{
    border-image: url(:/light/checkbox_checked.svg);
}

/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:exclusive:unchecked
{
    border-image: url(:/light/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:unchecked:selected
{
    border-image: url(:/Qss/light/radio_unchecked_disabled.svg);
}

QMenu::indicator:exclusive:checked
{
    border-image: url(:/light/radio_checked.svg);
}

QMenu::indicator:exclusive:checked:selected
{
    border-image: url(:/light/radio_checked.svg);
}

QMenu::right-arrow
{
    margin: 0.5ex;
    border-image: url(:/light/right_arrow.svg);
    width: 0.6ex;
    height: 0.9ex;
}


QWidget:disabled
{
    color: #454545;
    background-color: #EFF0F1;
}

QAbstractItemView
{
    alternate-background-color: #EFF0F1;
    color: #31363B;
    border: 0.1ex solid 3A3939;
    border-radius: 0.2ex;
}

QWidget:focus,
QMenuBar:focus
{
    border: 0.1ex solid #33A4DF;
}

QLineEdit
{
    background-color: #FCFCFC;
    padding: 0.5ex;
    border-style: solid;
    border: 0.1ex solid #BAB9B8;
    border-radius: 0.2ex;
    color: #31363B;
}

QAbstractScrollArea
{
    border-radius: 0.2ex;
    border: 0.1ex solid #BAB9B8;
    background-color: transparent;
}
QPlainTextEdit,QTextBrowser
{
    background-color: white;  /* */
    color: #31363B;
    border-radius: 0.2ex;
    border: 0.1ex solid #BAB9B8;
}

QHeaderView::section
{
    background-color: #BAB9B8;
    color: #31363B;
    padding: 0.5ex;
    border: 0.1ex solid #BAB9B8;
}

QMainWindow::separator
{
    background-color: #EFF0F1;
    color: white;
    padding-left: 0.4ex;
    spacing: 0.2ex;
    border: 0.1ex dashed #BAB9B8;
}

QMainWindow::separator:hover
{

    background-color: #787876;
    color: white;
    padding-left: 0.4ex;
    border: 0.1ex solid #BAB9B8;
    spacing: 0.2x;
}

QMenu::separator
{
    height: 0.1ex;
    background-color: #BAB9B8;
    color: white;
    padding-left: 0.4ex;
    margin-left: 1ex;
    margin-right: 0.5ex;
}


QToolBar
{
    border: 0.1ex transparent #393838;
    background: 0.1ex solid #EFF0F1;
    font-weight: bold;
}

QToolBar::handle:horizontal
{
    border-image: url(:/light/hmovetoolbar.svg);
    width = 1.6ex;
    height = 6.4ex;
}

QToolBar::handle:vertical
{
    border-image: url(:/light/vmovetoolbar.svg);
    width = 5.4ex;
    height = 1ex;
}

QToolBar::separator:horizontal
{
    border-image: url(:/light/hsepartoolbar.svg);
    width = 0.7ex;
    height = 6.3ex;
}

QToolBar::separator:vertical
{
    border-image: url(:/light/vsepartoolbars.svg);
    width = 6.3ex;
    height = 0.7ex;
}

QPushButton
{
    color: #31363B;
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #EFF0F1, stop: 0.5 #eaebec);
    border-width: 0.1ex;
    border-color: #BAB9B8;
    border-style: solid;
    padding: 0.5ex;
    border-radius: 0.2ex;
    outline: none;
}

QPushButton:disabled
{
    background-color: #e0e1e2;
    border-width: 0.1ex;
    border-color: #b4b4b4;
    border-style: solid;
    padding-top: 0.5ex;
    padding-bottom: 0.5ex;
    padding-left: 1ex;
    padding-right: 1ex;
    border-radius: 0.2ex;
    color: #b4b4b4;
}

QPushButton:focus
{
    color: black;
}

QPushButton:checked
{
    background-color: #BAB9B8;
    border-color: #6A6969;
}

QTabWidget{
    border: 0.1ex solid #BAB9B8;
}

/* BORDERS */
QTabWidget::pane
{
    padding: 0.5ex;
    margin: 0.1ex;
}

QTabWidget::pane:top
{
    border: 0.1ex solid #BAB9B8;
    top: -0.1ex;
}

QTabWidget::pane:bottom
{
    border: 0.1ex solid #BAB9B8;
    bottom: -0.1ex;
}

QTabWidget::pane:left
{
    border: 0.1ex solid #BAB9B8;
    right: -0.1ex;
}

QTabWidget::pane:right
{
    border: 0.1ex solid #BAB9B8;
    left: -0.1ex;
}

QTabBar
{
    qproperty-drawBase: 0;
    left: 0.5ex; /* move to the right by 0.5ex */
    border-radius: 0.3ex;
}

QTabBar:focus
{
    border: 0ex transparent black;
}

QTabBar::close-button
{
    border-image: url(:/light/close.svg);
    width: 1.2ex;
    height: 1.2ex;
    background: transparent;
}

QTabBar::close-button:hover
{
    border-image: url(:/light/close-hover.svg);
    width: 1.2ex;
    height: 1.2ex;
    background: transparent;
}

QTabBar::close-button:pressed
{
    border-image: url(:/light/close-pressed.svg);
    width: 1.2ex;
    height: 1.2ex;
    background: transparent;
}

/* TOP TABS */
QTabBar::tab:top
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-top: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    min-width: 5ex;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:last,
QTabBar::tab:top:only-one
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-right: 0.1ex solid #BAB9B8;
    border-top: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    min-width: 5ex;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:!selected
{
    color: #31363B;
    background-color: #D9D8D7;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:first:!selected
{
    color: #31363B;
    background-color: #D9D8D7;
    border: 0.1ex transparent black;
    border-top-left-radius: 0.2ex;
    border-top-right-radius: 0.2ex;
}

QTabBar::tab:top:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
    border-left: 0.1ex solid #BAB9B8;
}

QTabBar::tab:top:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
}

/* BOTTOM TABS */
QTabBar::tab:bottom
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-bottom: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-width: 5ex;
}

QTabBar::tab:bottom:last,
QTabBar::tab:bottom:only-one
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-right: 0.1ex solid #BAB9B8;
    border-bottom: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-width: 5ex;
}

QTabBar::tab:bottom:!selected
{
    color: #31363B;
    background-color: #D9D8D7;
    border: 0.1ex transparent black;
    border-left: 0.1ex solid #BAB9B8;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
}

QTabBar::tab:bottom:first:!selected
{
    color: #31363B;
    background-color: #D9D8D7;
    border: 0.1ex transparent black;
    border-bottom-left-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
}

QTabBar::tab:bottom:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
    border-left: 0.1ex solid #BAB9B8;
}

QTabBar::tab:bottom:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
}

/* LEFT TABS */
QTabBar::tab:left
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-right: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-height: 5ex;
}

QTabBar::tab:left:last,
QTabBar::tab:left:only-one
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-bottom: 0.1ex solid #BAB9B8;
    border-right: 0.1ex solid #BAB9B8;
    background-color: #EFF0F1;
    padding: 0.5ex;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
    min-height: 5ex;
}

QTabBar::tab:left:!selected
{
    color: #31363B;
    background-color: #D9D8D7;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-top-right-radius: 0.2ex;
    border-bottom-right-radius: 0.2ex;
}

QTabBar::tab:left:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
    border-top: 0.1ex solid #BAB9B8;
}

QTabBar::tab:left:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
}

/* RIGHT TABS */
QTabBar::tab:right
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-left: 0.1ex solid #BAB9B8;
    background-color: #D9D8D7;
    padding: 0.5ex;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
    min-height: 5ex;
}

QTabBar::tab:right:last,
QTabBar::tab:right:only-one
{
    color: #31363B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-bottom: 0.1ex solid #BAB9B8;
    border-left: 0.1ex solid #BAB9B8;
    background-color: #D9D8D7;
    padding: 0.5ex;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
    min-height: 5ex;
}

QTabBar::tab:right:!selected
{
    color: #31363B;
    background-color: #54575B;
    border: 0.1ex transparent black;
    border-top: 0.1ex solid #BAB9B8;
    border-top-left-radius: 0.2ex;
    border-bottom-left-radius: 0.2ex;
}

QTabBar::tab:right:!selected:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
    border-top: 0.1ex solid #BAB9B8;
}

QTabBar::tab:right:!selected:first:hover
{
    background-color: rgba(61, 173, 232, 0.1);
    border: 0.1ex rgba(61, 173, 232, 0.1);
}

QTabBar QToolButton::right-arrow:enabled
{
    border-image: url(:/light/right_arrow.svg);
}

QTabBar QToolButton::left-arrow:enabled
{
    border-image: url(:/light/left_arrow.svg);
}

QTabBar QToolButton::right-arrow:disabled
{
    border-image: url(:/light/right_arrow_disabled.svg);
}

QTabBar QToolButton::left-arrow:disabled
{
    border-image: url(:/light/left_arrow_disabled.svg);
}

QToolButton
{
    background-color: transparent;
    border: 0.1ex solid #BAB9B8;
    border-radius: 0.2ex;
    margin: 0.3ex;
    padding: 0.5ex;
}

QToolButton[popupMode="1"] /* only for MenuButtonPopup */
{
    padding-right: 2ex; /* make way for the popup button */
}

QToolButton[popupMode="2"] /* only for InstantPopup */
{
    padding-right: 1ex; /* make way for the popup button */
}

QToolButton::menu-indicator
{
    border-image: url(:/light/down_arrow.svg);
    top: -0.7ex; left: -0.2ex; /* shift it a bit */
    width = 0.9ex;
    height = 0.6ex;
}

QToolButton::menu-arrow
{
    border-image: url(:/light/down_arrow.svg);
    width = 0.9ex;
    height = 0.6ex;
}

QToolButton:hover,
QToolButton::menu-button:hover
{
    background-color: transparent;
    border: 0.1ex solid #33A4DF;
}

QToolButton:checked,
QToolButton:pressed,
QToolButton::menu-button:pressed
{
    background-color: #47b8fc;
    border: 0.1ex solid #47b8fc;
    padding: 0.5ex;
}

QToolButton::menu-button
{
    border: 0.1ex solid #BAB9B8;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    /* 1ex width + 0.4ex for border + no text = 2ex allocated above */
    width: 1ex;
    padding: 0.5ex;
    outline: none;
}

QToolButton::menu-arrow:open
{
    border: 0.1ex solid #BAB9B8;
}

QPushButton::menu-indicator
{
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
    left: 0.8ex;
}

QTableView
{
    border: 0.1ex solid #BAB9B8;
    gridline-color: #BAB9B8;
    background-color: #FCFCFC;
}


QTableView,
QHeaderView
{
    border-radius: 0px;
}

QTableView::item:pressed
{
    background: #33A4DF;
    color: #31363B;
}

QTableView::item:selected:active
{
    background: #33A4DF;
    color: #31363B;
}

QTableView::item:selected:hover
{
    background-color: #47b8f3;
    color: #31363B;
}

QListView::item:pressed,
QTreeView::item:pressed
{
    background: #3daee9;
    color: #31363B;
}

QTreeView::item:selected:active,
QListView::item:selected:active
{
    background: #3daee9;
    color: #31363B;
}

QListView::item:selected:hover,
QTreeView::item:selected:hover
{
    background-color: #51c2fc;
    color: #31363B;
}


QHeaderView
{
    background-color: #EFF0F1;
    border: 0.1ex transparent;
    border-radius: 0px;
    margin: 0px;
    padding: 0px;

}

QHeaderView::section
{
    background-color: #EFF0F1;
    color: #31363B;
    padding: 0.5ex;
    border: 0.1ex solid #BAB9B8;
    border-radius: 0px;
    text-align: center;
}

QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-top: 0.1ex solid #BAB9B8;
}

QHeaderView::section::vertical
{
    border-top: transparent;
}

QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one
{
    border-left: 0.1ex solid #BAB9B8;
}

QHeaderView::section::horizontal
{
    border-left: transparent;
}


QHeaderView::section:checked

 {
    color: black;
    background-color: #b9dae7;
 }

 /* style the sort indicator */
QHeaderView::down-arrow
{
    image: url(:/light/down_arrow.svg);
}

QHeaderView::up-arrow
{
    image: url(:/light/up_arrow.svg);
}

QTableCornerButton::section
{
    background-color: #EFF0F1;
    border: 0.1ex transparent #BAB9B8;
    border-radius: 0px;
}

QPushButton:hover
{
    border: 0.1ex solid #3daef3;
    color: #31363B;
}

QPushButton:focus
{
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #4cbdff, stop: 0.5 #33a4e8);
    color: white;
}

QPushButton:focus:hover
{
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #bedfec, stop: 0.5 #b9dae7);
    color: #31363B;
}

QPushButton:focus:pressed,
QPushButton:pressed
{
    background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #bedfec, stop: 0.5 #b9dae7);
    color: #31363B;
}

'''