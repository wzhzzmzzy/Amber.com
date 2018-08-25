function main(splash, args)
    splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    local ok, reason = splash:go("http://xk.liontao.xin")
    splash:wait(0.5)
    if ok then
        icode = splash:select("#icode")
        csrf = splash:select("input[type='hidden']")
        ok, csrf = csrf:field_value()
        return {
            icode = icode:png(),
            csrf = csrf,
            cookies = splash:get_cookies()
        }
    end
end