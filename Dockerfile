FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir ruff==0.15.1
COPY pyproject.toml main.py Game.py GameState.py Player.py Cards.py Deck.py ./
COPY test_game.py test_game_state.py ./
ENV GATOSIM_SAVE_PATH=/app/state/gamestate.json
RUN mkdir -p /app/state
VOLUME ["/app/state"]

CMD ["python", "main.py"]
