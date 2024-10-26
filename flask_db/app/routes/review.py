from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from ..models.review import Review
from ..connectors.db import db
import traceback

review = Blueprint('review', __name__)

@review.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    try:
        # Debug print
        print(f"Current user: {current_user.id}, Role: {current_user.role}")
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query based on user role
        if current_user.role == 'Admin':
            reviews = Review.query.order_by(Review.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
        else:
            reviews = Review.query.filter_by(user_id=current_user.id)\
                .order_by(Review.created_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)

        # Convert reviews to list of dictionaries
        reviews_list = []
        for review in reviews.items:
            reviews_list.append({
                'id': review.id,
                'product_id': review.product_id,
                'rating': review.rating,
                'description': review.description,
                'user_id': review.user_id,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Format data for template
        data = {
            'data': reviews_list,
            'meta': {
                'page': reviews.page,
                'pages': reviews.pages,
                'total': reviews.total,
                'prev_page': reviews.prev_num,
                'next_page': reviews.next_num,
                'has_prev': reviews.has_prev,
                'has_next': reviews.has_next
            }
        }

        print(f"Successfully fetched {len(reviews_list)} reviews")  # Debug print
        return render_template('reviews.html', reviews=data)

    except Exception as e:
        print(f"Error in get_reviews: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        return render_template('error.html', error=str(e)), 500

@review.route('/review', methods=['POST'])
@login_required
def create_review():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['product_id', 'rating', 'description']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        new_review = Review(
            product_id=data['product_id'],
            rating=data['rating'],
            description=data['description'],
            user_id=current_user.id
        )
        
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

@review.route('/review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        
        if current_user.role != 'Admin' and review.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting review: {str(e)}")
        return jsonify({'error': 'Failed to delete review'}), 500