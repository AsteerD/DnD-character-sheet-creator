import os
import sys
import webbrowser
from pathlib import Path

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject
from PyQt5 import QtWidgets

TEMPLATE_PATH = Path("5E_CharacterSheet_Fillable.pdf")  # <- Twój przesłany PDF
OUTPUT_PATH = Path("character_filled.pdf")


# --- PDF helper functions (pdfrw) ---
def get_pdf_fields(pdf_path):
    """Zwraca listę nazw pól znalezionych w formularzu (surowe nazwy)."""
    pdf = PdfReader(str(pdf_path))
    fields = []
    for page in pdf.pages:
        annots = page.Annots
        if not annots:
            continue
        for annot in annots:
            if annot.Subtype == PdfName.Widget and annot.get('/T'):
                raw = annot.get('/T')
                # raw zazwyczaj wygląda jak (FieldName) -> konwertujemy do czystego stringa
                name = str(raw)
                if name.startswith('(') and name.endswith(')'):
                    name = name[1:-1]
                fields.append(name)
    return sorted(set(fields))


def set_pdf_values(template_path, output_path, values_map):
    """
    values_map: dict z kluczami logicznymi (np. 'name', 'class', 'str') - ale
    funkcja stara się dopasować je heurystycznie do rzeczywistych nazw pól w PDF.
    """
    template = PdfReader(str(template_path))
    # wymusz appearance update by większość czytników zaktualizowała wyświetlanie
    if template.Root and template.Root.AcroForm:
        template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))

    # Normalize keys: lower-case for matching
    lowered = {k.lower(): str(v) for k, v in values_map.items()}

    def match_value_for_field(field_name):
        """Heurystyka: próbujemy dopasować wartość po nazwie pola."""
        fn = field_name.lower()
        # bezpośrednie dopasowania
        if "char" in fn and ("name" in fn or "character" in fn):
            return lowered.get("name") or lowered.get("charactername") or lowered.get("character")
        if "player" in fn and "name" in fn:
            return lowered.get("player")
        if "class" in fn or "classlevel" in fn:
            # jeśli pole ma też level w nazwie, podstawimy "Class Level"
            cl = lowered.get("class") or lowered.get("klass")
            level = lowered.get("level")
            if cl and level:
                return f"{cl} {level}"
            return cl or level
        if "subclass" in fn or "archetype" in fn:
            return lowered.get("subclass")
        if "align" in fn:
            return lowered.get("alignment")
        if fn.strip() in ("ac", "armor class", "armor"):
            return lowered.get("ac")
        # ability scores - różne warianty nazw pól
        for ab in ("str", "strength"):
            if ab in fn:
                return lowered.get("str") or lowered.get("strength")
        for ab in ("dex", "dexterity"):
            if ab in fn:
                return lowered.get("dex") or lowered.get("dexterity")
        for ab in ("con", "constitution"):
            if ab in fn:
                return lowered.get("con") or lowered.get("constitution")
        for ab in ("int", "intelligence"):
            if ab in fn:
                return lowered.get("int") or lowered.get("intelligence")
        for ab in ("wis", "wisdom"):
            if ab in fn:
                return lowered.get("wis") or lowered.get("wisdom")
        for ab in ("cha", "charisma"):
            if ab in fn:
                return lowered.get("cha") or lowered.get("charisma")
        # level
        if "level" in fn and "class" not in fn:
            return lowered.get("level")
        # fallback: sprawdź czy któraś z kluczowych nazw jest substringiem
        for k in lowered.keys():
            if k in fn:
                return lowered[k]
        return None

    for page in template.pages:
        annots = page.Annots
        if not annots:
            continue
        for annot in annots:
            if annot.Subtype == PdfName.Widget and annot.get('/T'):
                raw = annot.get('/T')
                name = str(raw)
                if name.startswith('(') and name.endswith(')'):
                    name = name[1:-1]
                value = match_value_for_field(name)
                if value is not None:
                    # ustawiamy wartość (V) i usuwamy starą appearance (/AP), żeby reader odświeżył
                    annot.update(PdfDict(V='({})'.format(value)))
                    if annot.get('/AP'):
                        try:
                            del annot['/AP']
                        except Exception:
                            pass

    PdfWriter().write(str(output_path), template)


# --- PyQt5 GUI ---
class CharacterDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Character Sheet -> PDF (demo)")
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QFormLayout()

        # podstawowe
        self.name_input = QtWidgets.QLineEdit()
        self.player_input = QtWidgets.QLineEdit()
        self.class_input = QtWidgets.QLineEdit()
        self.subclass_input = QtWidgets.QLineEdit()
        self.level_input = QtWidgets.QSpinBox()
        self.level_input.setRange(1, 20)
        self.alignment_input = QtWidgets.QLineEdit()
        self.ac_input = QtWidgets.QSpinBox()
        self.ac_input.setRange(0, 50)

        # ability scores
        self.str_input = QtWidgets.QSpinBox(); self.str_input.setRange(1, 30)
        self.dex_input = QtWidgets.QSpinBox(); self.dex_input.setRange(1, 30)
        self.con_input = QtWidgets.QSpinBox(); self.con_input.setRange(1, 30)
        self.int_input = QtWidgets.QSpinBox(); self.int_input.setRange(1, 30)
        self.wis_input = QtWidgets.QSpinBox(); self.wis_input.setRange(1, 30)
        self.cha_input = QtWidgets.QSpinBox(); self.cha_input.setRange(1, 30)

        layout.addRow("Character name", self.name_input)
        layout.addRow("Player name", self.player_input)
        layout.addRow("Class", self.class_input)
        layout.addRow("Subclass", self.subclass_input)
        layout.addRow("Level", self.level_input)
        layout.addRow("Alignment", self.alignment_input)
        layout.addRow("AC", self.ac_input)

        # abilities in a horizontal row
        h = QtWidgets.QHBoxLayout()
        h.addWidget(QtWidgets.QLabel("STR")); h.addWidget(self.str_input)
        h.addWidget(QtWidgets.QLabel("DEX")); h.addWidget(self.dex_input)
        h.addWidget(QtWidgets.QLabel("CON")); h.addWidget(self.con_input)
        h.addWidget(QtWidgets.QLabel("INT")); h.addWidget(self.int_input)
        h.addWidget(QtWidgets.QLabel("WIS")); h.addWidget(self.wis_input)
        h.addWidget(QtWidgets.QLabel("CHA")); h.addWidget(self.cha_input)
        layout.addRow("Abilities", h)

        # buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.export_btn = QtWidgets.QPushButton("Export to PDF")
        self.list_fields_btn = QtWidgets.QPushButton("List PDF fields (debug)")
        btn_layout.addWidget(self.list_fields_btn)
        btn_layout.addWidget(self.export_btn)
        layout.addRow(btn_layout)

        self.setLayout(layout)

        # signals
        self.export_btn.clicked.connect(self.on_export)
        self.list_fields_btn.clicked.connect(self.on_list_fields)

    def collect_values(self):
        return {
            "name": self.name_input.text(),
            "player": self.player_input.text(),
            "class": self.class_input.text(),
            "subclass": self.subclass_input.text(),
            "level": str(self.level_input.value()),
            "alignment": self.alignment_input.text(),
            "ac": str(self.ac_input.value()),
            "str": str(self.str_input.value()),
            "dex": str(self.dex_input.value()),
            "con": str(self.con_input.value()),
            "int": str(self.int_input.value()),
            "wis": str(self.wis_input.value()),
            "cha": str(self.cha_input.value()),
        }

    def on_list_fields(self):
        if not TEMPLATE_PATH.exists():
            QtWidgets.QMessageBox.warning(self, "Brak pliku", f"Nie mogę znaleźć pliku: {TEMPLATE_PATH}")
            return
        fields = get_pdf_fields(TEMPLATE_PATH)
        # pokaż okno z listą pól
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Pola formularza w PDF (debug)")
        v = QtWidgets.QVBoxLayout()
        text = QtWidgets.QPlainTextEdit()
        text.setPlainText("\n".join(fields))
        text.setReadOnly(True)
        v.addWidget(text)
        btn = QtWidgets.QPushButton("Close")
        btn.clicked.connect(dlg.accept)
        v.addWidget(btn)
        dlg.setLayout(v)
        dlg.resize(600, 400)
        dlg.exec_()

    def on_export(self):
        if not TEMPLATE_PATH.exists():
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Nie znaleziono szablonu PDF: {TEMPLATE_PATH}")
            return
        values = self.collect_values()
        try:
            set_pdf_values(TEMPLATE_PATH, OUTPUT_PATH, values)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd PDF", f"Wystąpił błąd przy zapisie PDF:\n{e}")
            return

        # spróbuj otworzyć plik wynikowy
        QtWidgets.QMessageBox.information(self, "Gotowe", f"Zapisano: {OUTPUT_PATH}")
        try:
            webbrowser.open_new(str(OUTPUT_PATH.resolve()))
        except Exception:
            pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = CharacterDemo()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
