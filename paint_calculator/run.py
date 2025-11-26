import json

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap

from paint_calculator.api import api, sanitize_input

app = Flask(__name__)
app.register_blueprint(api)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)


@app.route('/')
def index():
    """
    Loads the index page
    :return: Index page
    """
    return render_template("index.html")


@app.route('/dimensions', methods=['GET'])
def dimensions():
    """
    Sanitizes inputs from the first page and displays the Dimensions page
    :return: Dimensions page
    """
    rooms = request.args.get("rooms")
    if not rooms:
        flash('Please enter the number of rooms first.', 'warning')
        return redirect(url_for('index'))
    
    try:
        rooms = sanitize_input(rooms)
        if rooms <= 0:
            flash('Number of rooms must be at least 1.', 'warning')
            return redirect(url_for('index'))
        if rooms > 20:  # Reasonable limit to prevent abuse
            flash('Maximum of 20 rooms allowed. Please contact support for larger projects.', 'warning')
            return redirect(url_for('index'))
            
        return render_template("dimensions.html", rooms=rooms)
    except (ValueError, TypeError):
        flash('Please enter a valid number of rooms.', 'danger')
        return redirect(url_for('index'))

@app.route('/results', methods=['POST'])
def results():
    """
    Handles the form submission and displays the results
    :return: Results page or redirects if invalid data
    """
    try:
        dimensions_data = {}
        number_of_data_sets = int(len(request.form) / 3)
        
        if number_of_data_sets == 0:
            flash('No room data provided. Please try again.', 'warning')
            return redirect(url_for('index'))
        
        for i in range(number_of_data_sets):
            try:
                length = float(request.form.get(f'length-{i}', 0))
                width = float(request.form.get(f'width-{i}', 0))
                height = float(request.form.get(f'height-{i}', 0))
                
                if length <= 0 or width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive numbers")
                
                dimensions_data[f'room-{i+1}'] = {
                    'length': length,
                    'width': width,
                    'height': height
                }
            except (ValueError, TypeError) as e:
                flash(f'Invalid dimensions for room {i+1}. Please enter valid numbers greater than zero.', 'danger')
                return redirect(url_for('dimensions', rooms=number_of_data_sets))
        
        return render_template(
            "results.html",
            dimensions_data=dimensions_data,
            stored_data=json.dumps(dimensions_data)
        )
        
    except Exception as e:
        app.logger.error(f'Error processing results: {str(e)}')
        flash('An error occurred while processing your request. Please try again.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9200, debug=True)
