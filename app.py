from flask import Flask, render_template, request
from src.SearchEngine import SearchEngine
from src.Pagination import Pagination
from src.search_engine.main import se, rs, rel

app = Flask(__name__, template_folder="template", static_folder="static")

institutions = [
    "金融学院", "经济学院", "商学院", "法学院", "新闻学院", "信息学院"
]


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/search/')
def search():
    cur_page = request.args.get("page", default=1, type=int)
    query = request.args.get("q", default="", type=str)
    associate_switch = request.args.get("ast_sw", default="on", type=str)
    inst_filter = request.args.get("inst_filter", default="", type=str)
    if associate_switch == "on":
        requery = True
    else:
        requery = False

    if query == "":
        return render_template("index.html")
    search_engine = SearchEngine(query=query, requery=requery, inst_filter=inst_filter)
    search_engine.search()
    result_num, need_requery, origin_query, query, link_list, rel_people, rel_inst = search_engine.get_result(cur_page)
    pagination = Pagination(cur_page, result_num)
    return render_template("answer.html", query=query, need_requery=need_requery, origin_query=origin_query,
                           result_num=result_num, link_list=link_list, pagination=pagination, ast_sw=associate_switch,
                           rel_people=rel_people, rel_inst=rel_inst, institutions=institutions, inst_filter=inst_filter)


if __name__ == "__main__":
    se.load_reverse_index()
    se.load_title()
    rs.load_doc()

    app.run(host='0.0.0.0')
