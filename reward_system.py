import logging

def evaluate(action, success):
    reward = 1 if success else -1
    logging.info(f"REWARD: {reward} | AKSI: {action}")
    return reward

# Contoh penggunaan:
# evaluate("BUAT_FOLDER:/project_x", True)  # +1
# evaluate("EDIT_FILE:/data.txt", False)    # -1
