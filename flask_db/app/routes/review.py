from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models.review import Review
from ..connectors.db import db

review = Blueprint('review', __name__)

@review.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        if current_user.role == 'Admin':
            # Admin dapat melihat semua review dengan pagination
            pagination = Review.query.order_by(Review.created_at.desc()).paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
        else:
            # User biasa hanya bisa melihat review mereka sendiri dengan pagination
            pagination = Review.query.filter_by(user_id=current_user.id)\
                .order_by(Review.created_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert reviews to dictionary
        reviews_data = [{
            'id': review.id,
            'product_id': review.product_id,
            'rating': review.rating,
            'description': review.description,
            'user_id': review.user_id,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for review in pagination.items]

        # Add pagination metadata
        meta = {
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
            'prev_page': pagination.prev_num,
            'next_page': pagination.next_num,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next
        }

        return jsonify({
            'data': reviews_data,
            'meta': meta
        }), 200

    except Exception as e:
        print(f"Error getting reviews: {str(e)}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500

@review.route('/review', methods=['POST'])
@login_required
def create_review():
    try:
        data = request.get_json()
        
        # Validasi input
        if not all(key in data for key in ['product_id', 'rating', 'description']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        # Buat review baru
        new_review = Review(
            product_id=data['product_id'],
            rating=data['rating'],
            description=data['description'],
            user_id=current_user.id
        )
        
        # Simpan ke database
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': {
                'id': new_review.id,
                'product_id': new_review.product_id,
                'rating': new_review.rating,
                'description': new_review.description,
                'user_id': new_review.user_id,
                'created_at': new_review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating review: {str(e)}")
        return jsonify({'error': 'Failed to create review'}), 500

@review.route('/review/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        
        # Pastikan user hanya bisa update review miliknya sendiri
        if review.user_id != current_user.id and current_user.role != 'Admin':
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        
        if 'rating' in data:
            if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            review.rating = data['rating']
            
        if 'description' in data:
            review.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': {
                'id': review.id,
                'product_id': review.product_id,
                'rating': review.rating,
                'description': review.description,
                'user_id': review.user_id,
                'updated_at': review.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating review: {str(e)}")
        return jsonify({'error': 'Failed to update review'}), 500

@review.route('/review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        
        # Pastikan user hanya bisa delete review miliknya sendiri
        if review.user_id != current_user.id and current_user.role != 'Admin':
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting review: {str(e)}")
        return jsonify({'error': 'Failed to delete review'}), 500