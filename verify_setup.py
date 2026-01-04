"""
Verification script to ensure everything is set up correctly
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath} - NOT FOUND")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath):
        print(f"[OK] {description}: {dirpath}")
        return True
    else:
        print(f"[MISSING] {description}: {dirpath} - NOT FOUND")
        return False

def check_imports():
    """Check if all required packages can be imported"""
    packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('streamlit', 'streamlit'),
        ('fastapi', 'fastapi'),
        ('sklearn', 'scikit-learn'),
        ('plotly', 'plotly'),
        ('seaborn', 'seaborn'),
    ]
    
    all_ok = True
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print(f"[OK] {package_name} imported successfully")
        except ImportError:
            print(f"[MISSING] {package_name} - NOT INSTALLED (pip install {package_name})")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("E-Commerce Analytics Platform - Setup Verification")
    print("=" * 60)
    
    print("\n1. Checking Required Files:")
    print("-" * 60)
    files_ok = True
    files_ok &= check_file('Online_Retail.xlsx', 'Dataset')
    files_ok &= check_file('app.py', 'Streamlit Dashboard')
    files_ok &= check_file('api.py', 'FastAPI Backend')
    files_ok &= check_file('train_models.py', 'Model Training Script')
    files_ok &= check_file('requirements.txt', 'Requirements File')
    
    print("\n2. Checking Model Files:")
    print("-" * 60)
    models_ok = True
    models_ok &= check_file('models/churn_model.pkl', 'Churn Model')
    models_ok &= check_file('models/clv_model.pkl', 'CLV Model')
    models_ok &= check_file('models/churn_scaler.pkl', 'Churn Scaler')
    models_ok &= check_file('models/clv_scaler.pkl', 'CLV Scaler')
    
    print("\n3. Checking Python Packages:")
    print("-" * 60)
    imports_ok = check_imports()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if not files_ok:
        print("⚠️  Some required files are missing!")
        print("   Make sure Online_Retail.xlsx is in the project directory")
    
    if not models_ok:
        print("⚠️  ML models not found!")
        print("   Run: python train_models.py")
    
    if not imports_ok:
        print("⚠️  Some packages are missing!")
        print("   Run: pip install -r requirements.txt")
    
    if files_ok and models_ok and imports_ok:
        print("[SUCCESS] Everything looks good! You're ready to run the project.")
        print("\nNext steps:")
        print("  1. Start dashboard: streamlit run app.py")
        print("  2. Start API: uvicorn api:app --reload")
    else:
        print("\nPlease fix the issues above before running the project.")
        sys.exit(1)

if __name__ == "__main__":
    main()

