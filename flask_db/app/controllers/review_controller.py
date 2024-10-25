from flask import jsonify
from ..models.review import Review
from ..connectors.db import db
from sqlalchemy.exc import SQLAlchemyError

class ReviewController:
    @staticmethod
    def create_review(user_id, product_id, rating, description):
        try:
            if not all([user_id, product_id, rating, description]):
                return {
                    'status': 'error',
                    'message': 'All fields are required'
                }, 400

            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return {
                    'status': 'error',
                    'message': 'Rating must be an integer between 1 and 5'
                }, 400

            existing_review = Review.query.filter_by(
                user_id=user_id,
                product_id=product_id
            ).first()

            if existing_review:
                return {
                    'status': 'error',
                    'message': 'User has already reviewed this product'
                }, 400

            new_review = Review(
                user_id=user_id,
                product_id=product_id,
                rating=rating,
                description=description
            )

            db.session.add(new_review)
            db.session.commit()

            return {
                'status': 'success',
                'message': 'Review created successfully',
                'data': {
                    'review_id': new_review.id,
                    'user_id': new_review.user_id,
                    'product_id': new_review.product_id,
                    'rating': new_review.rating,
                    'description': new_review.description,
                    'created_at': new_review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Error creating review: {str(e)}'
            }, 500

    @staticmethod
    def get_all_reviews():
        try:
            reviews = Review.query.all()
            reviews_data = [{
                'review_id': review.id,
                'user_id': review.user_id,
                'product_id': review.product_id,
                'rating': review.rating,
                'description': review.description,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for review in reviews]

            return {
                'status': 'success',
                'data': reviews_data
            }, 200

        except SQLAlchemyError as e:
            return {
                'status': 'error',
                'message': f'Error retrieving reviews: {str(e)}'
            }, 500

    @staticmethod
    def get_review(review_id):
        try:
            review = Review.query.get(review_id)
            if not review:
                return {
                    'status': 'error',
                    'message': 'Review not found'
                }, 404

            return {
                'status': 'success',
                'data': {
                    'review_id': review.id,
                    'user_id': review.user_id,
                    'product_id': review.product_id,
                    'rating': review.rating,
                    'description': review.description,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 200

        except SQLAlchemyError as e:
            return {
                'status': 'error',
                'message': f'Error retrieving review: {str(e)}'
            }, 500

    @staticmethod
    def update_review(review_id, description, rating):
        try:
            review = Review.query.get(review_id)
            if not review:
                return {
                    'status': 'error',
                    'message': 'Review not found'
                }, 404

            if description:
                review.description = description
            if rating:
                if not isinstance(rating, int) or not (1 <= rating <= 5):
                    return {
                        'status': 'error',
                        'message': 'Rating must be an integer between 1 and 5'
                    }, 400
                review.rating = rating

            db.session.commit()

            return {
                'status': 'success',
                'message': 'Review updated successfully',
                'data': {
                    'review_id': review.id,
                    'user_id': review.user_id,
                    'product_id': review.product_id,
                    'rating': review.rating,
                    'description': review.description,
                    'updated_at': review.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Error updating review: {str(e)}'
            }, 500

    @staticmethod
    def delete_review(review_id):
        try:
            review = Review.query.get(review_id)
            if not review:
                return {
                    'status': 'error',
                    'message': 'Review not found'
                }, 404

            db.session.delete(review)
            db.session.commit()

            return {
                'status': 'success',
                'message': 'Review deleted successfully'
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Error deleting review: {str(e)}'
            }, 500
