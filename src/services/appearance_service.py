from services.theme_manager import set_appearance
VALID_MODES=("System","Light","Dark")
def set_appearance_mode(mode): return set_appearance(mode)
def get_appearance_mode():
    import customtkinter as ctk
    x=ctk.get_appearance_mode()
    return x if x in ("Light","Dark") else "System"
