from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, Conversation, Message
from .services import get_chat_response
import os
import io
import PyPDF2

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

# ── Main Chat Route ─────────────────────────────────────
@routes.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'GET':
        return render_template('chat.html')

    data = request.get_json()
    user_input = data.get('message')
    conversation_id = data.get('conversation_id')

    # Get or create the conversation
    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
    else:
        conversation = Conversation(user_id=current_user.id, title="New Chat")
        db.session.add(conversation)
        db.session.commit()

    # Store user message
    user_msg = Message(role='user', content=user_input, conversation_id=conversation.id)
    db.session.add(user_msg)

    # Build chat history
    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp).all()
    chat_history = [{"role": msg.role, "content": msg.content} for msg in messages]

    # Get bot response
    bot_reply = get_chat_response(chat_history)

    # Store bot message
    bot_msg = Message(role='assistant', content=bot_reply, conversation_id=conversation.id)
    db.session.add(bot_msg)

    db.session.commit()

    return jsonify({
        "response": bot_reply,
        "conversation_id": conversation.id
    })


# ── Conversation-detail route ─────────────────────────────
@routes.route('/conversations/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first_or_404()

    msgs = (
        Message.query.filter_by(conversation_id=conversation.id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    history = [{"role": m.role, "content": m.content} for m in msgs]
    return jsonify({"conversation_id": conversation.id, "messages": history})


# ── New: Upload & Summarize File ──────────────────────────
@routes.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1].lower()

    try:
        if file_ext == '.pdf':
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
        elif file_ext == '.txt':
            text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if not text.strip():
            return jsonify({"summary": "⚠️ File is empty or unreadable."})

        summary_prompt = f"Summarize the following content:\n\n{text[:4000]}"
        summary = get_chat_response([{"role": "user", "content": summary_prompt}])

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": "Failed to process file", "details": str(e)}), 500






