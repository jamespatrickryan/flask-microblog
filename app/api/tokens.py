from flask import jsonify

from app import db
from app.api import blueprint
from app.api.auth import basic_auth, token_auth


@blueprint.route('/tokens', methods=('POST',))
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})


@blueprint.route('/tokens', methods=('DELETE',))
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
