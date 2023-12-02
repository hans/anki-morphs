from typing import Callable, Optional

import aqt
from anki.tags import TagManager
from aqt import mw
from aqt.qt import (  # pylint:disable=no-name-in-module
    QDialog,
    QStandardItem,
    QStandardItemModel,
    QStyle,
    Qt,
)

from . import ankimorphs_constants
from .ui.tag_selection_ui import Ui_TagSelectionDialog


class TagSelectionDialog(QDialog):
    # The UI comes from ankimorphs/ui/tag_selection.ui which is used in Qt Designer,
    # which is then converted to ankimorphs/ui/tag_selection_ui.py,
    # which is then imported here.
    #
    # Here we make the final adjustments that can't be made (or are hard to make) in
    # Qt Designer, like setting up tables and widget-connections.

    def __init__(
        self,
    ) -> None:
        super().__init__(parent=None)  # no parent makes the dialog modeless
        assert mw is not None
        self.ui = Ui_TagSelectionDialog()  # pylint:disable=invalid-name
        self.ui.setupUi(self)  # type: ignore[no-untyped-call]
        self._all_tags: list[str] = TagManager(mw.col).all()
        self.selected_tags: list[str] = []
        self.current_row: int = -1
        self._model = QStandardItemModel()
        self._setup_buttons()

    def set_selected_tags_and_row(self, selected_tags: list[str], row: int) -> None:
        self.selected_tags = selected_tags
        self.current_row = row
        self._populate_tags_list()

    def _populate_tags_list(self) -> None:
        for index, tag in enumerate(self._all_tags):
            tag_item = QStandardItem(tag)
            tag_item.setCheckable(True)

            check_state = Qt.CheckState.Unchecked
            if tag in self.selected_tags:
                check_state = Qt.CheckState.Checked

            tag_item.setData(check_state, Qt.ItemDataRole.CheckStateRole)
            self._model.setItem(index, tag_item)

        self.ui.listView.setModel(self._model)

    def _setup_buttons(self) -> None:
        style: Optional[QStyle] = self.style()
        assert style is not None

        apply_icon = style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
        self.ui.applyButton.setIcon(apply_icon)

        self.ui.unselectAllButton.setAutoDefault(False)
        self.ui.applyButton.setAutoDefault(False)

        self.ui.unselectAllButton.clicked.connect(self._unselect_all_items)
        self.ui.applyButton.clicked.connect(self._save_selected_tags)

    def _unselect_all_items(self) -> None:
        for _row in range(self._model.rowCount()):
            _item = self._model.item(_row, column=0)
            assert _item is not None
            _item.setCheckState(Qt.CheckState.Unchecked)

    def _save_selected_tags(self) -> None:
        checked: list[str] = []
        for _row in range(self._model.rowCount()):
            _item = self._model.item(_row, column=0)
            assert _item is not None
            if _item.checkState() == Qt.CheckState.Checked:
                checked.append(_item.text())
        self.selected_tags = checked
        self.accept()

    def closeWithCallback(  # pylint:disable=invalid-name
        self, callback: Callable[[], None]
    ) -> None:
        # This is used by the Anki dialog manager
        self.close()
        aqt.dialogs.markClosed(ankimorphs_constants.TAG_SELECTOR_DIALOG_NAME)
        callback()
