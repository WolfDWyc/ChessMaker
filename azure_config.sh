RESOURCEGROUP="chessmaker"
SITENAME="chessmaker"

az webapp config set --resource-group $RESOURCEGROUP --name $SITENAME --startup-file "export PYTHONPATH="${PYTHONPATH}:." && python chessmaker/clients/pywebio_ui.py"
