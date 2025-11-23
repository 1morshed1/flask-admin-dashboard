from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from app.models import FileCategory, ActivityLog
from app.schemas.file_category_schema import (
    FileCategoryCreateSchema,
    FileCategoryUpdateSchema,
    FileCategoryQuerySchema
)
from app.utils.validation import validate_json_body, validate_query_params

file_categories_bp = Blueprint('file_categories', __name__, url_prefix='/api/file-categories')


def require_admin():
    """Decorator to require admin or superadmin role"""
    claims = get_jwt()
    role = claims.get('role', 'user')
    if role not in ['admin', 'superadmin']:
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': 'Admin access required'
            }
        }), 403
    return None


def _paginate_firestore(query_results, page, per_page):
    """Helper function to paginate Firestore results"""
    total = len(query_results)
    start = (page - 1) * per_page
    end = start + per_page
    items = query_results[start:end]
    pages = (total + per_page - 1) // per_page
    
    return {
        'items': items,
        'total': total,
        'pages': pages,
        'has_next': end < total,
        'has_prev': page > 1
    }


@file_categories_bp.route('', methods=['GET'])
@jwt_required()
@validate_query_params(FileCategoryQuerySchema)
def get_file_categories(validated_data: FileCategoryQuerySchema):
    """Get all file categories with pagination and filtering"""
    # Get all file categories
    all_categories = FileCategory.get_all()
    
    # Apply filters
    filtered_categories = all_categories
    
    # Search filter
    if validated_data.search:
        search_term = validated_data.search.lower()
        filtered_categories = [
            cat for cat in filtered_categories
            if (hasattr(cat, 'code') and search_term in cat.code.lower()) or
               (hasattr(cat, 'name') and cat.name and search_term in cat.name.lower()) or
               (hasattr(cat, 'description') and cat.description and search_term in cat.description.lower())
        ]
    
    # Status filter
    if validated_data.status:
        filtered_categories = [cat for cat in filtered_categories if hasattr(cat, 'status') and cat.status == validated_data.status]
    
    # Sorting
    sort_field = validated_data.sort
    reverse = validated_data.order == 'desc'
    
    def get_sort_value(cat):
        if hasattr(cat, sort_field):
            value = getattr(cat, sort_field)
            if isinstance(value, datetime):
                return value.timestamp() if value else 0
            return value if value else ''
        return ''
    
    filtered_categories.sort(key=get_sort_value, reverse=reverse)
    
    # Pagination
    pagination = _paginate_firestore(filtered_categories, validated_data.page, validated_data.per_page)

    return jsonify({
        'file_categories': [cat.to_dict() for cat in pagination['items']],
        'pagination': {
            'page': validated_data.page,
            'per_page': validated_data.per_page,
            'total': pagination['total'],
            'pages': pagination['pages'],
            'has_next': pagination['has_next'],
            'has_prev': pagination['has_prev']
        }
    }), 200


@file_categories_bp.route('', methods=['POST'])
@jwt_required()
@validate_json_body(FileCategoryCreateSchema)
def create_file_category(validated_data: FileCategoryCreateSchema):
    """Create a new file category"""
    error = require_admin()
    if error:
        return error

    # Normalize code to uppercase
    code = validated_data.code.upper()

    # Check if code already exists
    if FileCategory.code_exists(code):
        return jsonify({
            'error': {
                'code': 'CATEGORY_EXISTS',
                'message': 'A file category with this code already exists'
            }
        }), 409

    # Create file category
    file_category = FileCategory(
        code=code,
        name=validated_data.name or code,
        description=validated_data.description,
        status=validated_data.status
    )
    file_category.save()

    # Log activity
    current_user_id = get_jwt_identity()
    activity = ActivityLog(
        event_type='file_category_created',
        user_id=current_user_id,
        description=f'Created file category: {file_category.code}',
        ip_address=request.remote_addr
    )
    activity.save()

    return jsonify({
        'message': 'File category created successfully',
        'file_category': file_category.to_dict()
    }), 201


@file_categories_bp.route('/<category_id>', methods=['GET'])
@jwt_required()
def get_file_category(category_id):
    """Get a specific file category by ID"""
    file_category = FileCategory.get_by_id(category_id)
    if not file_category:
        return jsonify({
            'error': {
                'code': 'CATEGORY_NOT_FOUND',
                'message': f'File category with id {category_id} not found'
            }
        }), 404

    return jsonify(file_category.to_dict()), 200


@file_categories_bp.route('/<category_id>', methods=['PUT'])
@jwt_required()
@validate_json_body(FileCategoryUpdateSchema)
def update_file_category(category_id, validated_data: FileCategoryUpdateSchema):
    """Update a file category"""
    error = require_admin()
    if error:
        return error

    file_category = FileCategory.get_by_id(category_id)
    if not file_category:
        return jsonify({
            'error': {
                'code': 'CATEGORY_NOT_FOUND',
                'message': f'File category with id {category_id} not found'
            }
        }), 404

    # Update fields
    if validated_data.code:
        # Normalize code to uppercase
        code = validated_data.code.upper()
        # Check if new code already exists
        if FileCategory.code_exists(code, exclude_id=category_id):
            return jsonify({
                'error': {
                    'code': 'CATEGORY_EXISTS',
                    'message': 'A file category with this code already exists'
                }
            }), 409
        file_category.code = code

    if validated_data.name is not None:
        file_category.name = validated_data.name

    if validated_data.description is not None:
        file_category.description = validated_data.description

    if validated_data.status:
        file_category.status = validated_data.status

    file_category.save()

    # Log activity
    current_user_id = get_jwt_identity()
    activity = ActivityLog(
        event_type='file_category_updated',
        user_id=current_user_id,
        description=f'Updated file category: {file_category.code}',
        ip_address=request.remote_addr
    )
    activity.save()

    return jsonify({
        'message': 'File category updated successfully',
        'file_category': file_category.to_dict()
    }), 200


@file_categories_bp.route('/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_file_category(category_id):
    """Delete a file category"""
    error = require_admin()
    if error:
        return error

    file_category = FileCategory.get_by_id(category_id)
    if not file_category:
        return jsonify({
            'error': {
                'code': 'CATEGORY_NOT_FOUND',
                'message': f'File category with id {category_id} not found'
            }
        }), 404

    # Check if category is assigned to any users
    user_count = file_category.get_user_count()
    if user_count > 0:
        return jsonify({
            'error': {
                'code': 'CATEGORY_IN_USE',
                'message': f'Cannot delete file category. It is assigned to {user_count} user(s). Please unassign it from all users first.'
            }
        }), 400

    code = file_category.code
    file_category.delete()

    # Log activity
    current_user_id = get_jwt_identity()
    activity = ActivityLog(
        event_type='file_category_deleted',
        user_id=current_user_id,
        description=f'Deleted file category: {code}',
        ip_address=request.remote_addr
    )
    activity.save()

    return jsonify({
        'message': 'File category deleted successfully'
    }), 200

